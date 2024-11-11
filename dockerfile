# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Update and install required packages
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y wkhtmltopdf && \
    apt-get clean

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Create a virtual environment and install the required packages
RUN python3 -m venv myenv && \
    myenv/bin/pip install --no-cache-dir -r requirements.txt

# Make port 8501 available to the world outside this container
EXPOSE 8501

# Run the Streamlit app when the container launches using the virtual environment
CMD ["myenv/bin/python", "-m", "streamlit", "run", "GlauDec.py"]

