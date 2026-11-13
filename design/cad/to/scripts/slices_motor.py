from slices import slices
W="../work/motor/"
slices(W+"motor_result.npz","../motor_mount_slices.png",xs=[-10.5,-8,-5.5,-3.5,-2,-0.7],ys=[0,9.5],zs=[110,118],dz=1.2,title="MotorMount BESO slices (x = fore-aft, forward = -x)")
