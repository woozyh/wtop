## wtop
A simple basic system resource monitor for Unix/Linux like Operating Systems which supports /proc.
<hr>

## Installation 
Not necessary but you need to install ```nvidia-ml-py``` so just try ```pip install -r requirements.txt```. <br><br>
**Note:** By default program supports nvidia gpus since i have one so if you want to show your own you can rewrite the program **(this is the rule of open source softwares)**. Program is just reading data from /proc so you don't want need extra packages, but the gpus drivers are not open source softwares and because of that the ```nvidia-ml-py``` module used and it's the first and last dependency that you need to install for nvidia and if you are not nvidia user just ommit the gpu part or you can rewrite it for yourself and if you want to share it with others just fork and do it.
