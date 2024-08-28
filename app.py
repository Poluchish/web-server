from flask import Flask, request, jsonify, render_template
import json
import os
import importlib
import inspect

app = Flask(__name__)

@app.route('/json/<module>/<function>', methods=['POST'])
def process_json(module, function):
    """Обработка JSON через указанный модуль и функцию."""
    try:
        # Динамическая загрузка модуля
        module = importlib.import_module(f'modules.{module}')
        
        # Динамическое получение функции
        func = getattr(module, function)
        
        # Получение данных из запроса
        data = request.get_json()
        
        # Вызов функции с данными
        result = func(data['data'])
        
        return jsonify(result)
    
    except ModuleNotFoundError:
        return "Unknown module NAME", 500
    except AttributeError:
        return "Unknown function NAME", 500

@app.route('/html/')
def list_functions():
    """Отображение всех доступных функций в модулях."""
    functions_info = []
    
    # Перебор всех файлов в папке modules
    for filename in os.listdir('modules'):
        if filename.endswith('.py'):
            module_name = filename[:-3]
            module = importlib.import_module(f'modules.{module_name}')
            for attr in dir(module):
                if not attr.startswith('__'):
                    func = getattr(module, attr)
                    functions_info.append({
                        'module': module_name,
                        'function': attr,
                        'description': func.__doc__,
                        'code': inspect.getsource(func) 
                    })
    
    return render_template('functions.html', functions=functions_info)

if __name__ == '__main__':
    app.run(debug=True)
