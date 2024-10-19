from setuptools import setup, find_packages
from pathlib import Path

# Đọc file README.md nếu bạn có để mô tả về dự án
# Đọc requirements từ file
with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name="AI_measure",
    version="1.0.0",
    description="AI model for body measurement predictions",
    long_description_content_type="text/markdown",
    author="Your Name",
    author_email="your.email@example.com",
    url="https://github.com/yourusername/AI_measure",  # Thay thế URL của dự án GitHub
    packages=find_packages(where='src'),  # Tìm tất cả các package trong thư mục src
    package_dir={'': 'src'},  # Thư mục chứa code là src
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'AI_measure=AI_measure.main:main',  # Điểm vào chính của project
        ],
    },
    python_requires='>=3.7',  # Yêu cầu Python phiên bản nào
    include_package_data=True,  # Bao gồm các file không phải code như README, LICENSE
)
