# InCore services API Document
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
## data collection service
- Folder location: `src/resources/dataService`
- Description: this service contains **upload**, **download** service
### upload service
- File location: `src/resources/dataService/upload.py`
- Description: This py is a upload API. When uploading a file, the service will check the file type and project type. Then generate a file UID. After that, the service will check the file content with checkers in `src/resources/dataService/fileChecker.py`.
- Usage: Call the API with `POST` with a form
    ```
    {
        'file': binary file,
        'type': project type (defined in params),
        'tokenstr': The random token string,
        'tokenint': The converted token value
    }
    ```
    and get a response
    ```
    {
        'status': 'success' or 'error',
        'msg': error msg,
        'data':{
            'fileUid': the generated file uid
        }
    }
    ```
- Acceptable file types and their rules:
  - Numerical project: A `csv` with column name and their values. The values should be numerical data. For example:
    ```
    temp,humidity,quantity
    30.57,43,6
    22.89,99,30
    ```
  - NLP project: A `tsv` with column name. There should be a column named **"value"** which contains the numerical value. For example:
    ```
    Sentence1	value
    I am happy	1
    I am sad	0
    ```
    or
    ```
    Sentence1	Sentence2	value
    I am happy	So am I :)	1
    I am happy	I am a student	0
    ```
  - CV project: A `zip` file. There should be a (only one) `csv` file in the zip directly, not in a folder. There should be a column that contains the numerical value and named **"value"**. Other columns are the image file path (related path in zip). For example:
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
