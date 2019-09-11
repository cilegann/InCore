import os
import json
from parse import *
import warnings
from tokenize import generate_tokens


acceptableType={
    "num":["regression","classification","clustering","abnormal"],
    "cv":["regression","classification"],
    "nlp":["regression","classification"]
}
acceptableLib=["sklearn","keras"]
acceptableParamType=["int","float","bool","enum","string"]
acceptableIOType=["float","classifiable","string","path"]
for root,ds,_ in os.walk("./analyticAlgoWarehouse"):
    for d in ds:
        fl=os.listdir(os.path.join(root,d))
        assert len(fl)==2
        filename=fl[0][:fl[0].rfind(".")]
        for f in fl:
            assert filename in f, "Files' name are not the same"
        jsonFile=os.path.join(os.path.join(root,d,filename+'.json'))
        pyFile=os.path.join(os.path.join(root,d,filename+'.py'))
        assert os.path.isfile(jsonFile)
        assert os.path.isfile(pyFile)
        j=json.load(open(jsonFile))
        assert "dataType" in j, "dataType not defined in json"
        assert j["dataType"] in acceptableType,"dataType not supported. Check spelling"
        assert "projectType" in j, "projectType not defined in json"
        assert j["projectType"] in acceptableType[j["dataType"]], "projectType not supported. Check spelling"
        assert "algoName" in j, "algoName not defined in json"
        assert j["algoName"]==filename, "algoName defined in json must be identical with filename"
        assert "description" in j, "description not defined in json"
        assert "lib" in j, "lib not defined in json"
        assert j["lib"] in acceptableLib, "lib not supported, Check spelling"
        assert "param" in j, "param not defined in json"
        assert type(j["param"]) is list, "param must be a list"
        for p in j["param"]:
            assert "name" in p, f"attribute 'name' missing in {p}"
            assert "description" in p, f"attribute 'description' missing in {p}"
            assert "type" in p, f"attribute 'type' missing in {p}"
            assert p["type"] in acceptableParamType, f"type {p['type']} not supported, check spelling"
            assert "default" in p,f"attribute 'default' missing in {p}"
            if p["type"]=="int":
                assert "upperBound" in p, f"attribute 'upperBound' not found in {p}"
                assert "lowerBound" in p, f"attribute 'lowerBound' not found in {p}"
                assert int(p["upperBound"])==p["upperBound"], f"upperBound must be int"
                assert int(p["lowerBound"])==p["lowerBound"], f"lowerBound must be int"
                assert int(p["default"])==p["default"], f"default must be int"
            if p["type"]=="float":
                assert "upperBound" in p, f"attribute 'upperBound' not found in {p}"
                assert "lowerBound" in p, f"attribute 'lowerBound' not found in {p}"
                assert float(p["upperBound"])==p["upperBound"], f"upperBound must be float"
                assert float(p["lowerBound"])==p["lowerBound"], f"lowerBound must be float"
                assert float(p["default"])==p["default"], f"default must be float"
            if p["type"]=="bool":
                assert (p["default"]==1 or p["default"]==0), f"default must be 0 or 1"
            if p["type"]=="enum":
                assert "list" in p, f"attribute 'list' not found in {p}"
                assert p["default"] in p["list"], f"default value not in list"
        assert "input" in j, "input not defined in json"
        for p in j["input"]:
            assert "name" in p, "attribute 'name' not found"
            assert "description" in p, f"attribute 'description' not found in {p}"
            assert "type" in p, f"attribure 'type' not found in {p}"
            assert p["type"] in acceptableIOType, f"type {p['type']} is not acceptable"
            assert "amount" in p, f"attribute 'amount' not found in {p}"
            assert p["amount"] in ["multiple","single"], f"amount {p['amount']} is not acceptable"
        assert "output" in j, "output not defined in json"
        for p in j["output"]:
            assert "name" in p, f"attribute 'name' not found in {p}"
            assert "description" in p, f"attribute 'description' not found in {p}"
            assert "type" in p, f"attribure 'type' not found in {p}"
            assert p["type"] in acceptableIOType, f"type {p['type']} is not acceptable"
            assert "amount" not in p, "output has no attribute 'amount'"
        paramList=[p["name"] for p in j["param"]]
        inputList=[p["name"] for p in j["input"]]
        outputList=[p["name"] for p in j["output"]]
        
        g=generate_tokens(open(pyFile).readline)
        record=[]
        for typ,syn,start,end,line in g:
            if typ==1 or typ==53 or typ==3:
                record.append((typ,syn,start,end,line))
        p=[]
        i=[]
        o=[]
        for ii in range(len(record[:-3])):
            if record[ii][0]==1 and record[ii+1][0]==53 and record[ii+2][0]==3 and record[ii+3][0]==53:
                if record[ii][1]=='param':
                    p.append(record[ii+2])
                if record[ii][1]=='inputData':
                    i.append(record[ii+2])
                if record[ii][1]=='outputData':
                    o.append(record[ii+2])
        pWarn=0
        iWarn=0
        oWarn=0
        for pp in p:
            if pp[1].replace(" ","").replace("'","").replace('"',"") not in paramList:
                print(f"[Warning][PyFile Syntax] param key error at {pp[2]}~{pp[3]}: {pp[1]}")
                pWarn+=1
        for ii in i:
            if ii[1].replace(" ","").replace("'","").replace('"',"") not in inputList:
                print(f"[Warning][PyFile Syntax] inputData key error at {ii[2]}~{ii[3]}: {ii[1]}")
                iWarn+=1
        for oo in o:
            if oo[1].replace(" ","").replace("'","").replace('"',"") not in outputList:
                print(f"[Warning][PyFile Syntax] outputData key error at {oo[2]}~{oo[3]}: {oo[1]}")
                oWarn+=1
        print("\n**********************************************************")
        print(f"Algo [{filename}] checked with result:\n")
        print(f"  > JSON   : OK")
        print(f"  > Python : \n      {pWarn} param key warnings\n      {iWarn} inputData key warnings\n      {oWarn} outputData key warnings")
        print(f"\n### IMPORTANT: This is just a simple key checker, please check again by yourself.")
        print("               If you are sure with your code, just ignore the warnings")
        print("**********************************************************\n")