import os
import json
import warnings
from tokenize import generate_tokens
from params import params
import logging

def algoChecker():
    param=params()

    acceptableType=param.dataProjectType
    acceptableLib=["sklearn","keras"]
    acceptableParamType=["int","float","bool","enum","string"]
    acceptableIOType=["float","classifiable","string","path"]
    reg=json.load(open(param.analyticAlgoReg))
    logging.info("[checkAlgo] Start")
    print("---------------------------------------------------")
    for dl in acceptableType:
        for pl in acceptableType[dl]:
            if not os.path.isdir(os.path.join(param.analyticServiceRoot,"core","analyticCore",dl,pl)):
                pass
            else:
                fl=os.listdir(os.path.join(param.analyticServiceRoot,"core","analyticCore",dl,pl))
                filenames=[f[:f.rfind(".")] for f in fl]
                filenames=list(set(filenames))
                for filename in filenames:
                    jsonFile=os.path.join(param.analyticServiceRoot,"core","analyticCore",dl,pl,filename+".json")
                    pyFile=os.path.join(param.analyticServiceRoot,"core","analyticCore",dl,pl,filename+".py")
                    assert os.path.isfile(jsonFile),f"{jsonFile} not found"
                    assert os.path.isfile(pyFile),f"{pyFile} not found"
                    if filename not in reg[dl][pl]:
                        logging.warning(f"{dl}.{pl}.{filename} not in Reg")
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
                            assert p['upperBound']>p['lowerBound'], f"upperBound must be greater than lowerBound"
                        if p["type"]=="float":
                            assert "upperBound" in p, f"attribute 'upperBound' not found in {p}"
                            assert "lowerBound" in p, f"attribute 'lowerBound' not found in {p}"
                            assert float(p["upperBound"])==p["upperBound"], f"upperBound must be float"
                            assert float(p["lowerBound"])==p["lowerBound"], f"lowerBound must be float"
                            assert float(p["default"])==p["default"], f"default must be float"
                            assert p['upperBound']>p['lowerBound'], f"upperBound must be greater than lowerBound"
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
                    pWarn=[]
                    iWarn=[]
                    oWarn=[]
                    notUsedWarn=[]
                    usedParam=[]
                    for pp in p:
                        usedParam.append(pp[1].replace(" ","").replace("'","").replace('"',""))
                        if pp[1].replace(" ","").replace("'","").replace('"',"") not in paramList:
                            pWarn.append(f"[Syntax] param key error at {pp[2]}~{pp[3]}: {pp[1]}")
                    for ii in i:
                        if ii[1].replace(" ","").replace("'","").replace('"',"") not in inputList:
                            iWarn.append(f"[Syntax] inputData key error at {ii[2]}~{ii[3]}: {ii[1]}")
                    for oo in o:
                        if oo[1].replace(" ","").replace("'","").replace('"',"") not in outputList:
                            oWarn.append(f"[Syntax] outputData key error at {oo[2]}~{oo[3]}: {oo[1]}")
                    for pp in paramList:
                        if pp not in usedParam:
                            notUsedWarn.append(f"[Not used] param '{pp}' defined in json is not used in python")
                    if len(iWarn)==0 and len(oWarn)==0 and len(pWarn)==0 and len(notUsedWarn)==0:
                        print(f"Algo [{filename}] checked with result: OK")
                    else:
                        print(f"Algo [{filename}] checked with result:")
                        print(f"  > JSON   : OK")
                        print(f"  > Python : ")
                        print(f"      {len(pWarn)} param key warning")
                        for pw in pWarn:
                            print(f"        -{pw}")
                        print(f"      {len(iWarn)} inputData key warning")
                        for iw in iWarn:
                            print(f"        -{iw}")
                        print(f"      {len(oWarn)} outputData key warning")
                        for ow in oWarn:
                            print(f"        -{ow}")
                        print(f"      {len(notUsedWarn)} not used param warning")
                        for nw in notUsedWarn:
                            print(f"        -{nw}")
    print("---------------------------------------------------")

if __name__=="__main__":
    algoChecker()