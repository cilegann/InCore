import logging
def tokenValidator(string,token):
    logging.debug(f'[util token] Token str:{string} Token int:{token}')
    for i,s in enumerate(string):
        token-=(i+1)*ord(s)
    return (token==0)