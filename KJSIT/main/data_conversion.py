def conversion(hist):
    params = {}
    rec = []
    for record in hist:
        obj = [
            record['timestamp'],
            record['app'],
            record['disease'],
            record['result'],
            record['probability'],
        ]
        rec.append(obj)
    rec.reverse()
    sz = len(rec)
    params = {'records' : rec, 'size' : sz}
    return params