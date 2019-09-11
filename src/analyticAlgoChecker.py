import os
from params import params
import json
param=params()

acceptableType={
    "num":["regression","classification","clustering","abnormal"],
    "cv":["regression","classification"],
    "nlp":["regression","classification"]
}
acceptableLib=["sklearn","keras"]
acceptableParamType=["int","float","bool","enum","string"]

for root,ds,_ in os.walk("./analyticAlgoWarehouse"):
    for d in ds:
        fl=os.listdir(os.path.join(root,d))
        assert len(fl)==2
        filename=fl[0][:filename.rfind(".")]
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
            if p[]
        assert "input" in j, "input not defined in json"
        assert "output" in j, "output not defined in json"
