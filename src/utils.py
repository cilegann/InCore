def tokenValidator(string,token):
    for i,s in enumerate(string):
        token-=(i+1)*ord(s)
    return (token==0)