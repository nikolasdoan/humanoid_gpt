# run this in order

conda create --name h_gpt python=3.8

conda activate h_gpt 

# if no conda available

python --version
>>Python 3.8.10

sudo apt install python3.8-venv

python -m venv gpt

source gpt/bin/activate

# install dependencies

sudo apt-get install portaudio19-dev

sudo apt-get install python3-dev

pip install pyaudio

pip install -r requirements.txt


# create .env file for API key in the dustin-gpt folder
echo "OPENAI_API_KEY=your-secret-api-key" > .env

# run the server file in terminal A
python test_server.py

# run the client file in terminal B
python test_client.py
