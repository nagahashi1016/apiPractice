from fastapi import FastAPI, Query,  HTTPException
from typing import List, Dict, Any,Optional
from fastapi.middleware.cors import CORSMiddleware
import sqlite3

app = FastAPI()

origins = ["*"] 

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"], 
)

def db_connection(database_name):
    try:
        conn = sqlite3.connect(database_name)
        return conn
    except sqlite3.Error as e:
        print(e)
        return None


def map_column(index_mapping, row):
    return {index_mapping[i]: value for i, value in enumerate(row)}

#GET
@app.get("/get/", response_model=List[Dict[str, Any]])
def get_data_camera(
    id: int = Query(None, description="Camera ID"),
    name: str = Query(None, description="Camera name"),
    type: str = Query(None, description="Camera type"),
    sensorSize: str = Query(None, description="Sensor size"),
    pixelNumber: int = Query(None, description="Pixel number"),
    maker: str = Query(None, description="Camera maker"),
    lensMounts: str = Query(None, description="Lens mounts"),
    imageSta: str = Query(None, description="Image stabilization"),
    price: int = Query(None, description="Camera price"),
    releaseDate: str = Query(None, description="Release date"),
    URL: str = Query(None, description="Camera URL"),
):
    conn = db_connection("dataAPI.sqlite")
    cursor = conn.cursor()

    query = "SELECT * FROM camera WHERE 1=1"
    params = []

    if id is not None:
        query += " AND id = ?"
        params.append(id)

    if name:
        query += " AND name = ?"
        params.append(name)

    if type:
        query += " AND type = ?"
        params.append(type)

    if sensorSize:
        query += " AND sensorSize = ?"
        params.append(sensorSize)

    if pixelNumber is not None:
        query += " AND pixelNumber = ?"
        params.append(pixelNumber)

    if maker:
        query += " AND maker = ?"
        params.append(maker)

    if lensMounts:
        query += " AND lensMounts = ?"
        params.append(lensMounts)

    if imageSta:
        query += " AND imageSta = ?"
        params.append(imageSta)

    if price is not None:
        query += " AND price = ?"
        params.append(price)

    if releaseDate:
        query += " AND releaseDate = ?"
        params.append(releaseDate)

    if URL:
        query += " AND URL = ?"
        params.append(URL)

    cursor.execute(query, params)
    data = cursor.fetchall()

    column_names = ["id", "name", "type", "sensorSize", "pixelNumber", "maker", "lensMounts", "imageSta", "price", "releaseDate", "URL"]
    result = [map_column(column_names, row) for row in data]

    return result


#POST
def get_max_id():
    try:
        conn = db_connection("dataAPI.sqlite")
        cursor = conn.cursor()

        query = "SELECT MAX(id) FROM camera"
        cursor.execute(query)

        max_id = cursor.fetchone()[0]

        return max_id if max_id is not None else 0
    except Exception as e:
        print(f"Error getting max id: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

def post_data(
    id: int,
    name: str,
    type: str,
    sensorSize: str,
    pixelNumber: int ,
    maker: str ,
    lensMounts: str ,
    imageSta: str ,
    price: int,
    releaseDate: str,
    URL: str
):
    try:
        conn1 = db_connection("dataAPI.sqlite")
        cursor1 = conn1.cursor()

        query = """
        INSERT INTO camera (id, name, type, sensorSize, pixelNumber, maker, lensMounts, imageSta, price, releaseDate, URL)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        params = (id, name, type, sensorSize, pixelNumber, maker, lensMounts, imageSta, price, releaseDate, URL)
        print(params)
        cursor1.execute(query,params)
        conn1.commit()

        return {"message": "データを追加しました。"}
    except Exception as e:
        print(f"Error during database insertion: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@app.post("/post/")
def insert_data(
    name: str = Query(None, description="Camera name"),
    type: str = Query(None, description="Camera type"),
    sensorSize: str = Query(None, description="Sensor size"),
    pixelNumber: int = Query(None, description="Pixel number"),
    maker: str = Query(None, description="Camera maker"),
    lensMounts: str = Query(None, description="Lens mounts"),
    imageSta: str = Query(None, description="Image stabilization"),
    price: int = Query(None, description="Camera price"),
    releaseDate: str = Query(None, description="Release date"),
    URL: str = Query(None, description="Camera URL"),
):
    try:
        max_id = get_max_id()

        new_id = max_id + 1

        result = post_data(
            new_id, name, type, sensorSize, pixelNumber, maker, lensMounts, imageSta, price, releaseDate, URL
        )

        return {"message": f"データを追加しました。"}
    except HTTPException as e:
        raise e
    except Exception as e:
        print(f"Error during data insertion: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


#PATCH/UPDATE
@app.patch("/patch/", response_model=None)
def patch_data_camera(
    name: Optional[str] = Query(None, description="New value for name"),
    type: Optional[str] = Query(None, description="Camera type to identify the record to update"),
    sensorSize: Optional[str] = Query(None, description="New value for sensorSize"),
    pixelNumber: Optional[int] = Query(None, description="New value for pixelNumber"),
    maker: Optional[str] = Query(None, description="New value for maker"),
    lensMounts: Optional[str] = Query(None, description="New value for lensMounts"),
    imageSta: Optional[str] = Query(None, description="New value for imageSta"),
    price: Optional[int] = Query(None, description="New value for price"),
    releaseDate: Optional[str] = Query(None, description="New value for releaseDate"),
    URL: Optional[str] = Query(None, description="New value for URL"),
    where_id: Optional[int] = Query(None, description="Additional condition for WHERE clause on ID"),
):
    conn2 = db_connection("dataAPI.sqlite")
    cursor2 = conn2.cursor()
    set_values = []
    where_conditions = []

    if name is not None:
        set_values.append(f"name = '{name}'")
    if type is not None:
        set_values.append(f"type = '{type}'")
    if sensorSize is not None:
        set_values.append(f"sensorSize = '{sensorSize}'")
    if pixelNumber is not None:
        set_values.append(f"pixelNumber = {pixelNumber}")
    if maker is not None:
        set_values.append(f"maker = '{maker}'")
    if lensMounts is not None:
        set_values.append(f"lensMounts = '{lensMounts}'")
    if imageSta is not None:
        set_values.append(f"imageSta = '{imageSta}'")
    if price is not None:
        set_values.append(f"price = {price}")
    if releaseDate is not None:
        set_values.append(f"releaseDate = '{releaseDate}'")
    if URL is not None:
        set_values.append(f"URL = '{URL}'")

    if where_id is not None:
        where_conditions.append(f"id = {where_id}")

    set_clause = ", ".join(set_values)
    where_clause = " AND ".join(where_conditions) if where_conditions else ""

    print("SET Clause:", set_clause)
    print("WHERE Clause:", where_clause)

    query = f"UPDATE camera SET {set_clause}"
    if where_clause:
        query += f" WHERE {where_clause}"
    print("Final query:", query)
    cursor2.execute(query)
    conn2.commit()

    return {"message": "データを更新しました。"}


#DELETE
@app.delete("/delete/")
def delete_data_camera(
    id: Optional[int] = Query(None, description="Camera ID to identify the record to delete"),
):
    conn = db_connection("dataAPI.sqlite")
    cursor = conn.cursor()

    where_conditions = []

    if id is not None:
        where_conditions.append(f"id = {id}")

    if where_conditions:
        where_clause = " OR ".join(where_conditions)
        query_delete = f"DELETE FROM camera WHERE {where_clause}"
        query_update = f"UPDATE camera SET id = id - 1 WHERE id > {id}"

        try:
        
            cursor.execute(query_delete)
            
            cursor.execute(query_update)

            conn.commit()
            return {"message": f"データを削除しました。"}
        except Exception as e:
            print(f"Error during deletion and update: {e}")
            conn.rollback()
            raise HTTPException(status_code=500, detail="Internal Server Error")
    else:
        return {"message": "No conditions provided for deletion"}


