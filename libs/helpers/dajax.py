#-*- coding: utf-8 -*-

def clear_form_errors(dajax, form_id):
    dajax.add_data(form_id, 'dajaxiceFormClearErrors')

def set_form_errors(dajax, form_id, errors):
    
    data = {'formId' : form_id, 'globalErrors' : [], 'fieldsErrors' : {}}
    
    for field, errors in errors.iteritems():
        
        if field == '__all__':
            for error in errors:
                data['globalErrors'].append(error)
            
            continue
        
        for error in errors:
            try:
                data['fieldsErrors'][field].append(error)
            except KeyError:
                data['fieldsErrors'][field] = [error]
        
    if len(data['fieldsErrors'].keys()) == 0:
        del data['fieldsErrors']
        
    if len(data['globalErrors']) == 0:
        del data['globalErrors']
        
    dajax.add_data(data, 'dajaxiceFormSetErrors')