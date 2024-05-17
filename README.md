Resposta dada à "[Melhor forma de acessar sublistas para realizar operações de estatísticas](https://pt.stackoverflow.com/q/594576/196624)", leia no [stackoverflow](https://pt.stackoverflow.com/a/594640/196624) ou [aqui](answer.md).

# RMI

_Dada uma `lista`, calcule a maior média entre as sublistas, de forma que a próxima sublista é `lista[i: i+k]`._ 

No total haverá $len(lista)-k+1$ sublistas.

Fiz a implementação usando CPython API em C++ para demonstrar a diferença entre ela e o Python puro.

## Como usar

1. Crie um ambiente virtual: <a href="#ambiente-virtual-e-configurações-básicas">Ambiente virtual e Configurações Básicas</a>
2. Escolha um dos seguintes metodos: <a href="#instalação-e-execução">Instalação e Execução</a> ou <a href="#compilação">Compilação</a>

### Ambiente virtual e Configurações Básicas
``` bash
$ python3 -m venv env                           # Crie um ambiente virtual
# Ativação, escolha o da sua plataforma
$ source env/bin/activate                       # Linux
$ .\env\Scripts\activate                        # Windows
#
$ python -m pip install --upgrade pip           # Atualize o pip
```

### Instalação e Execução
```bash
$ python -m build --sdist                       # Irá gera o pacote do codigo cpython na pasta `dist`
$ python -m pip install .\dist\rmi-0.0.1.tar.gz # Instale ele no ambiente virtual
$ python test_time.py                           # Execute o teste
```

### Compilação
Pode também apenas compilar o modulo da seguinte forma:
```bash
$ python .\setup.py build                      # Irá compilar rmi/c_src/c_rmi.cpp na pasta `build/lib.**`
```

Copie o modulo (`.pyd`) da pasta `build/lib.**/rmi/`  para a pasta [src/rmi/](src/rmi/), exemplo:
```bash
$ cp build/lib.win-amd64-cpython-312/rmi/c_rmi.cp312-win_amd64.pyd src/rmi/
```

E execute:

```bash
$ python test_time.py                           # Execute o teste
```

## Dev

## compilação

É nessário o c++20 para compilar o arquivo [c_rmi.cpp](c_src/c_rmi.cpp), pois utiliza Designated initializers, veja a o parametro `extra_compile_args` da instânciação `module = Extension`, em [setup.py](setup.py).

## tests

Teste o modulo usando pytest e tox.
```bash
$ python -m pip install -U tox  # instale o tox no ambiente virtual
$ tox                           # execute os testes
```