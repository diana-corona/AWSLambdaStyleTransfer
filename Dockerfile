# Pull the base image with python 3.8 as a runtime for your Lambda
FROM public.ecr.aws/lambda/python:3.8

# Install OS packages for Pillow-SIMD
RUN yum -y install tar gzip zlib freetype-devel \
    gcc \
    ghostscript \
    lcms2-devel \
    libffi-devel \
    libimagequant-devel \
    libjpeg-devel \
    libraqm-devel \
    libtiff-devel \
    libwebp-devel \
    make \
    openjpeg2-devel \
    rh-python36 \
    rh-python36-python-virtualenv \
    sudo \
    tcl-devel \
    tk-devel \
    tkinter \
    which \
    xorg-x11-server-Xvfb \
    zlib-devel \
    && yum clean all

# Copy the earlier created requirements.txt file to the container
COPY app/requirements.txt ./app/

# Install the python requirements from requirements.txt
RUN python3.8 -m pip install -r ./app/requirements.txt
# Replace Pillow with Pillow-SIMD to take advantage of AVX2
RUN pip uninstall -y pillow && CC="cc -mavx2" pip install -U --force-reinstall pillow-simd

# Download model and store it in a directory
# RUN mkdir ./app/model
# RUN curl -L https://tfhub.dev/google/magenta/arbitrary-image-stylization-v1-256/2?tf-hub-format=compressed -o ./app/model/stylization.tar.gz
# RUN tar -xf ./app/model/stylization.tar.gz -C ./app/model/
# RUN rm -r ./app/model/stylization.tar.gz

# Copy the  files to the container
COPY app/ ./app


# Set the CMD to your handler
CMD ["app/style_image.lambda_handler"]
