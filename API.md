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

## Data collection service
- Folder location: `src/resources/dataService`
- Description: this service contains **upload**, **download** API


<details>
<summary>[API] upload</summary>

- File location: `src/resources/dataService/upload.py`
- Description: This py is a upload API. When uploading a file, the service will check the file type and project type. Then generate a file UID. After that, the service will check the file content with checkers in `src/resources/dataService/fileChecker.py`.
- Usage: Call the API with `GET http://host/download` with a form
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
  - NLP project: A `tsv` with column name. For project with label, there should be at least one column  which contains the numerical value. For example:
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
  - CV project: A `zip` file. There should be a (only one) `csv` file in the zip directly, not in a folder. For project with label, here should be at least one column that contains the numerical value. Other columns are the image file path (related path in zip). For example:
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
<summary>[API] download</summary>

- File location: `src/resources/dataService/download.py`
- Description: This py is a download API. When being request a file IDuploading a file, the service will return the binary file and renamed to the given file name.
- API: Call the API with `POST http://host/download` with a form
    ```
    {
        'fileUid': file id,
        'fileName': file name,
        'tokenstr': The random token string,
        'tokenint': The converted token value
    }
    ```
    and get a binary response

    ```
    </details>
    ```

<details>
<summary>[Method] file uid generator</summary>

- File location: `src/resources/dataService/utils.py`
- Description: Generate unique file id
- Usage: 

    `from resources.dataService.utils import fileUidGenerator`
    `uid=fileUidGenerator().uid`

</details>

<details>
<summary>[Method] file checker</summary>

- File location: `src/resources/dataService/utils.py`
- Description: Validate file content
- Usage: 

    `from resources.dataService.utils import fileUidGenerator`
    `fileCheck=fileChecker(savedPath,prjtype).check()`
</details>

<details>
<summary>[API] getColumn</summary>

- File location: `src/resources/dataService/getColumn.py`
- Description: Get column names and type
- API: Call the API with `POST http://host/download` with a form
    ```
    {
        'fileUid': file id,
        'type': project type (defined in params),
        'tokenstr': The random token string,
        'tokenint': The converted token value
    }
    ```
    get a json
    ```
    {
        'status': 'success' or 'error',
        'msg': error msg,
        'data':{
            'cols':[
                {
                    'name':'col1_name',
                    'type': col1_type (num/path/sentence)
                }
            ]
        }
    }
    ```
</details>

<details>
<summary>[API] getFileStatus</summary>
</details>

## Analytic Service

<details>
<summary> [API] doPreprocess</summary>

</details>

<details>
<summary> [API] getPreprocessPreview</summary>

</details>

<details>
<summary> [API] getCorrelation</summary>

</details>

<details>
<summary> [API] doSelection</summary>

</details>

<details>
<summary> [API] getAlgoList</summary>

</details>

<details>
<summary> [API] getAlgoParam</summary>

</details>

<details>
<summary> [API] doModelTrain</summary>

</details>

<details>
<summary> [API] doModelPredict</summary>

</details>

<details>
<summary> [API] doModelTest</summary>

</details>

<details>
<summary> [API] getModelStatus</summary>

</details>

<details>
<summary> [API] getModelFailReason</summary>

</details>

<details>
<summary> [API] getModelPreview</summary>

</details>


## Visualize Service