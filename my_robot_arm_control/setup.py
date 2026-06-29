from setuptools import find_packages, setup

package_name = 'my_robot_arm_control'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='enovo',
    maintainer_email='enovo@todo.todo',
    description='Control scripts for my_robot_arm',
    license='MIT',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'move_to_pose = my_robot_arm_control.move_to_pose:main',
        ],
    },
)
