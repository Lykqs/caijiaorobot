import launch
import launch_ros
from ament_index_python.packages import get_package_share_directory
import os

def generate_launch_description():
    #获取默认的urdf路径
    urdf_package_path =get_package_share_directory('lykbot_dstion')
    urdf_path=os.path.join(urdf_package_path,'urdf','fishbot.urdf')
    default_rviz_config_path =os.path.join(urdf_package_path,'config','display_robot_model.rviz')
    #生成一个urdf目录的参数，方面修改
    action_declare_arg_mode_path=launch.actions.DeclareLaunchArgument(

        name='model',default_value=str(urdf_path),description='加载文件路进'

    )
    #通过文件获取文件的内容，并转换成参数值对象，一共传入robot_state_publisher
    #1.通过文件的路径获取文件的内容
    Command_result=launch.substitutions.Command(['xacro ',launch.substitutions.LaunchConfiguration('model')])
    #2。转化为参数值对象
    robot_value=launch_ros.parameter_descriptions.ParameterValue(Command_result,value_type=str)

    action_robot_state_publisher = launch_ros.actions.Node(

        package= 'robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[{'robot_description': robot_value}]

    )
    action_joint_state_publisher = launch_ros.actions.Node(

        package= 'joint_state_publisher',
        
        executable='joint_state_publisher',
        

    )
    action_rviz_node = launch_ros.actions.Node(

        package = 'rviz2',
        executable = 'rviz2',
        arguments=['-d', default_rviz_config_path]
    )
    return launch.LaunchDescription([
        action_declare_arg_mode_path,
        action_robot_state_publisher,
        action_joint_state_publisher,
        action_rviz_node,


    ])