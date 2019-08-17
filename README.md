InCore services API Document
===

<style type="text/css">
.apiok{
color:#04B486
}
.methodok{
color:#01A9DB
}
.building{
color:#FCCF46
}
.scheduled{
color:#BDBDBD
}
</style>


## About Document
<font class='apiok'>Tested API</font>
<font class='building'>Building API</font>
<font class='methodok'>Tested Method</font>
<font class='scheduled'>Scheduled</font>

## Run
- Under `incore` folder, run `python3 apps.py`

## About Token
When requesting a service, the request should contain a random `tokenstr` and its `tokenint` to validate the request source.
The algorithm to convert `tokenstr` to `tokenint` is
```
tokenint=0
for i from 0 to len(tokenstr):
    tokenint+=((i+1) * ascii(tokenstr[i]))
```
The validator is `tokenValidator` in `src/utils.py`

## Parameters setting
- file location: `src/params.py`
- Description: File folder, model folder, acceptable files, acceptable projects are defined in this file. 
- Usage: In each py
  - use `from params import params` to import
  - create instance `param=params()`
  - Then get var with `param.var`

## Data collection service
- Folder location: `src/service/dataService`
- Description: this service contains **upload**, **download**, **getColumn**, **getFileStatus**, **delete** API


<details>
<summary class='apiok'>[API] dataUpload</summary>

- File location: `src/service/dataService/controller/upload.py`
- Description: This py is a upload API. When uploading a file, the service will check the file type and project type. Then generate a file UID. After that, the service will check the file content with checkers in `src/resources/dataService/fileChecker.py`.
- ==**Usage**==: `POST http://host/data/upload` with a form

    ```
    {
        'file': binaryFile,
        'type': dataType ( num/cv/nlp),
        'tokenstr': The_random_token_string,
        'tokenint': The_converted_token_value
    }
    ```
    and get a response
    ```
    {
        'status': 'success' or 'error',
        'msg': error_msg,
        'data':{
            'fileUid': the_generated_file_uid
        }
    }
    ```
- Acceptable file types and their rules:
  - **Numerical project**: A `csv` with column name and their values. The values should be numerical data. For example:
    ```
    temp,humidity,quantity
    30.57,43,6
    22.89,99,30
    ```
  - **NLP project**: A `tsv` with column name. For project with label, there should be at least one column  which contains the numerical value. For example:
    ```
    Sentence1	value	value2
    I am happy	1	1
    I am sad	0	0
    ```
    or
    ```
    Sentence1	Sentence2	value
    I am happy	So am I :)	1
    I am happy	I am a student	0
    ```
  - **CV project**: A `zip` file. There should be a (only one) `csv` file in the zip directly, not in a folder. For project with label, here should be at least one column that contains the numerical value. Other columns are the image file path (related path in zip). For example:
    ```
    file.zip
        |--lables.csv
        |--folder_foo
        |    |--imga.jpg
        |    |--imgb.png
        |
        |--folder_bar
        |    |--imgk.JPEG
        |    |--imgl.png
        |--imgt.jpg
    ```
    and the csv is
    ```
    filepath,value
    folder_foo/imga.jpg,1
    folder_foo/imgb.png,1
    folder_bar/imgk.JPEG,0
    folder_bar/imgl.png,0
    imgt.jpg,1
    ```
</details>



<details>
<summary class='apiok'>[API] dataDownload</summary>

- File location: `src/service/dataService/controller/download.py`
- Description: Download file
- ==**Usage**==: `GET http://host/data/download` with a form

    ```
    {
        'fileUid': file_id,
        'fileName': file_name (optional)
    }
    ```
    and get a binary response

</details>


<details>
<summary class='apiok'>[API] dataDelete</summary>


- File location: `src/service/dataService/controller/delete.py`
- Description: Delete file
- ==**Usage**==: `POST http://host/data/delete` with a form

    ```
    {
        'fileUid': file_id,
        'tokenstr': The_random_token_string',
        'tokenint': The_converted_token_value
    }
    ```
    get a json
    ```=json
    {
        'status': 'success' or 'error',
        'msg': error_msg,
        'data':{}
    }
    ```
</details>



<details>
<summary class='apiok'>[API] getColumn</summary>

- File location: `src/service/dataService/controller/getColumn.py`
- Description: Get column names and types
- ==**Usage**==: `POST http://host/data/getcol` with a form

    ```
    {
        'fileUid': file_id,
        'tokenstr': The_random_token_string,
        'tokenint': The_converted_token value
    }
    ```
    get a json
    ```
    {
        'status': 'success' or 'error',
        'msg': error_msg,
        'data':{
            'cols':[
                {
                    'name': col1_name,
                    'type': col1_type  (int/float/path/string)
                }
            ]
        }
    }
    ```
</details>

<details>
<summary class='apiok'>[API] getFileStatus</summary>

- File location: `src/service/dataService/controller/getFileStatus.py`
- Description: Get file (batch) status 
- ==**Usage**==: `POST http://host/data/getstatus` with a form

    ```
    {
        'fileUid': [file_id1, file_id2],
        'tokenstr': The_random_token_string',
        'tokenint': The_converted_token value
    }
    ```
    get a json
    ```
    {
        'status': 'success' or 'error',
        'msg': error_msg,
        'data':{
            'status':[status1(0/1),status2(0/1)]
        }
    }
    ```
    0 for not in-use, 1 for in-use
</details>



<details>
<summary class='methodok'>[Method] fileUidGenerator</summary>

- File location: `src/service/dataService/utils.py`
- Description: Generate unique file id
- Usage: 

    ```python
    from service.dataService.utils import fileUidGenerator
    uid=fileUidGenerator().uid
    ```

</details>

<details>
<summary class='methodok'>[Method] fileChecker</summary>

- File location: `src/service/dataService/utils.py`
- Description: Validate file content
- Usage: 

    ```python
    from service.dataService.utils import fileChecker
    fileCheck=fileChecker(savedPath,dataType).check()
    ```
</details>

<details>
<summary class='methodok'>[Method] getColType</summary>

- File location: `src/service/dataService/utils.py`
- Description: Get column names and type
- Usage: 

    ```python
    from service.dataService.utils import getColType
    coltype=getColType(savedPath,dataType).check()
    ```
    This is how `coltype` looks like:
    ```
    [
        {
            'name':col1_name,
            'type':col1_type (int/float/string)
        },
        {
            'name':col2_name,
            'type':col2_type (int/float/string)
        }...
    ]

    ```
</details>

<details>
<summary class='methodok'>[Method] getDf</summary>

- File location: `src/service/dataService/utils.py`
- Description: Get column names and type
- Usage: 

    ```python
    from service.dataService.utils import getColType
    data=getDf(savedPath,dataType).get()['data']
    ```
    
    Data is a dataframe.
</details>

## Visualize Service
- filelocation: `src/resources/visualizationService`
- Description: Use `bokeh` to show data and image. If the data is not supported by bokeh, it will return the image result of `matplotlib` and shown by bokeh.<br>For showing `bokeh` with `js`, please refer to _section 2_ of [this article](https://blog.csdn.net/cooldiok/article/details/85273652?fbclid=IwAR1fdXZ9k5FdqXq82sEWd3Lexe1vmiPr1ZDMad2Qvvv9xAakJWwozIWeRZo).

<details>
<summary class='apiok'> [API] getDataVisList</summary>

- File location: `src/service/visualizeService/controller/doDataviz.py`
- Description: get data visualize algorithm
- ==**Usage**==: `GET http://host/viz/data/getalgo`

    get a json

    ```
    {
            'status': 'success' or 'error',
            'msg': error_msg,
            'data':{
                {
                    "algos":[
                        {
                            "friendlyname":"algoname1",
                            "lib":"used lib",
                            "algoname":"algo1",
                            "data":{
                                "x":"float", -> need a x col and must be float or int
                                "y":"string", -> need a y col and must be string
                                "value":"none" -> not needed
                            },
                            "description":"2D line plot" -> algo description
                        },
                        {
                            "friendlyname":"algoname2",
                            "lib":"used lib",
                            "algoname":"algo2",
                            "data":{
                                "x":"int", -> need a x col and must be int
                                "y":"path", -> need a y col and must be path
                                "value":"float" -> need a value col and must be float
                            },
                            "description":"2D scatter plot" -> algo description
                        }
                    ]
                }
            }
    }
    ```
</details>

<details>
<summary class='methodok'> [CORE] dataViz</summary>

- File location: `src/service/visualizeService/core/dataViz.py`
</details>


<details>
<summary class='apiok'> [API] dataViz</summary>

- File location: `src/service/visualizeService/controller/dataViz.py`
- Description: Visualizing data
- ==**Usage**==: `POST http://host/viz/data/do` with param

    ```
    {
        'fileUid': fileID,
        'algoname': algoname,
        'datacol': {
            'x':'col_name1',
            'y':'col_name2',
            'value':'col_name3'
        }
        'tokenstr': The_random_token_string,
        'tokenint': The_converted_token value
    }
    ```
    
    and get a response
    
    ```
    {
        'status': 'success' or 'error',
        'msg': error_msg,
        'data':{
            'div': div of bokeh,
            'script': script of bokeh
        }
    }
    ```
</details>

<details>
<summary class='apiok'> [API] getImg</summary>

- File location: `src/service/visualizeService/controller/getImg.py`
- Description: Get binary img
- ==**Usage**==: `GET http://host/viz/getimg` with param

    ```
    uid='imguid'
    action='get'/'download'
    ```
</details>

## Analytic Service

### Preprocess and Data info

<details>
<summary class='methodok'> [CORE] missingFiltering</summary>

- File location: `src/service/analuticService/core/preprocess/missingFiltering.py`
- Discription: Filt missing value of number, string and path.
- ==**Usage**==: 
    - `filtCols` get a filted data
        Args: 
        - data: A 2D array of data
        - coltype: colType(int, float, string, path) respectivly
        - doList: filt the column or not
        - pathBase: the base folder of CV file. (OPTIONAL)
        ``` 
        filted_data=missingFitering().filtCols(
            [[dataCol1],[dataCol2]..],
            ["dataColType1","dataColType1"],
            [True,False],
            pathBase_of_CV
        )
        ```

        get a 2D array of filted data
    - `getRetainIndex` get which row to be retained
        Args:
        - data: A 2D array of data to check missing value
        - coltype: there colType
        - pathBase: the base folder of CV file. (OPTIONAL)
        ```
        retainIndex=missingFiltering().getRetainIndex(
            [[dataCol1],[dataCol2]..],
            ["dataColType1","dataColType1"],
            pathBase_of_CV
        )
        ```
        
        get a 1D np array of retain or not
</details>

<details>
<summary class='methodok'> [CORE] normalize</summary>

- File location: `src/service/analuticService/core/preprocess/normalize.py`
- Discription: Normalize the column
- ==**Usage**==: 
    
    Call imeplemented algo class, `do` to normalize
    
    Args: 
    - data: A 1D array of data
    
    ``` 
    data=normalizeAlgo(data).do()
    ```

    get a 1D array of normalized data
</details>

<details>
<summary class='methodok'> [CORE] outlierFiltering</summary>


- File location: `src/service/analuticService/core/preprocess/outlierFiltering.py`
- Discription: Filt outlier
- ==**Usage**==: 
    
    Call imeplemented algo class, `getRetainIndex` get which row to be retained
    
    Args:
    - data: A 1D array of data to check missing value
    ```
    retainIndex=outlierFilteringAlgo(data,algoName).getRetainIndex()
    ```
    get a 1D np array of retain or not
</details>




<details>
<summary class='methodok'> [CORE] stringCleaning</summary>

- File location: `src/service/analuticService/core/preprocess/stringCleaning.py`
- Discription: Clean string
- ==**Usage**==: 

    Call imeplemented algo class, `do` to get a clean string
    
    Args:
    - data: A string
    ```
    cleanedString=stringCleaningAlgo(data,algoName).do()
    ```
    get a 1D np array of retain or not
</details>


<details>
<summary style="color:#BDBDBD"> [API] getNormalizeMethod</summary>

</details>


<details>
<summary style="color:#BDBDBD"> [API] doPreprocess</summary>

- missing value
- normalize (multiple methods)
- outlier (multi methods)
- nlp: clean string (同時接受多個選項)
</details>

<details>
<summary style="color:#BDBDBD"> [API] getPreprocessPreview</summary>

</details>

<details>
<summary style="color:#BDBDBD"> [API] getCorrelation</summary>

</details>

### Training

<details>
<summary style="color:#BDBDBD"> [API] getAlgoList</summary>

</details>

<details>
<summary style="color:#BDBDBD"> [API] getAlgoParam</summary>

</details>

<details>
<summary style="color:#BDBDBD"> [API] doModelTrain</summary>
- 記: corre method, algo, params, columns
</details>


### After training
<details>
<summary style="color:#BDBDBD"> [API] doModelPredict</summary>

</details>

<details>
<summary style="color:#BDBDBD"> [API] doModelTest</summary>

</details>

<details>
<summary style="color:#BDBDBD"> [API] deleteModel</summary>

</details>

<details>
<summary style="color:#BDBDBD"> [API] getModelStatus</summary>

</details>

<details>
<summary style="color:#BDBDBD"> [API] getModelFailReason</summary>

</details>

<details>
<summary style="color:#BDBDBD"> [API] getModelPreview</summary>

</details>


## Database
- Engine`MYSQL`
- U:P@H `ican:roomno@1080Ti`
- Schema`incore`
- Tables
    - files: 
    `fid,dataType,path,status`
    - models: 
    `mid,dataType,projectType,status,PID`
- Connection in this project
    ```python=
    from utils import sql

    db=sql()
    
    #write
    db.cursor.execute("some sql here")
    db.conn.commit()

    #rollback
    db.conn.rollback()

    #read
    db.cursor.execute("select * from ...")
    data=[[dd for dd in d] for d in db.conn.fetchall()]
    
    #close
    db.conn.close()
    ```

