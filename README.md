# 1.A create conda environment

conda create --name h_gpt python=3.8

conda activate h_gpt 

# 1.B if no conda available

python --version
>>Python 3.8.10

sudo apt install python3.8-venv

python -m venv h_gpt

source h_gpt/bin/activate

# 2. install dependencies

pip install -r requirements.txt 

# 3. config API key (in humanoid_gpt folder)  
echo "OPENAI_API_KEY=your-secret-api-key" > .env 

# 4. configure remote robot server (optional overrides)
echo "SERVER_HOST=192.168.x.xx" >> .env
echo "SERVER_PORT=yyyy" >> .env

# 5. local test pair (binary protocol)
python scripts/test_server.py
# in another terminal
python scripts/test_client.py

# 6. run the TPC/IP server on the robot
python humanoid_server.py

# run the TPC/IP client
python scripts/humanoid_client.py

