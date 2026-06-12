FROM ubuntu:22.04

RUN apt-get update && apt-get install -y \
    libx11-6 libxcursor1 libxinerama1 libxrandr2 libxi6 \
    libgl1 libasound2 libpulse0 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY server.x86_64 .
COPY *.pck ./

RUN chmod +x server.x86_64

CMD ["./server.x86_64", "--headless"]    
