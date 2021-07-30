## Results

graphs: in ```graphs/``` folder

statistics: printed on standard output (stdout)

my last run statistics: ```report.txt```

## Dependencies

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install:

```bash
python3 -m pip install numpy
python3 -m pip install matplotlib
```

## Usage (Mac, Linux)

1.) in ```cec_2020.py``` use ```CEC20_SO_LIB = "./cec20_test_func.so"```

2.) ```c++ -fPIC -shared -o cec20_test_func.so cec20_test_func.cpp```

3.) ```python3 cec_2020.py```

## Usage (Windows)

1.) in ```cec_2020.py``` use ```CEC20_SO_LIB = "./cec20_test_func.dll"```

2.) ```c++ -fPIC -shared -o cec20_test_func.dll cec20_test_func.cpp```

3.) ```py cec_2020.py```
