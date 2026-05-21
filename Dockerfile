FROM python:3.9

# কাজের ডিরেক্টরি সেট করা
WORKDIR /code

# রিকোয়ারমেন্ট ফাইল কপি ও ইনস্টল করা
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# বাকি সব কোড কপি করা
COPY . .

# অ্যাপ রান করার কমান্ড
CMD ["python", "app.py"]