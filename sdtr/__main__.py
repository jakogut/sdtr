import cv2
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Simulated Distance Target Renderer')
    parser.add_argument('--target-path', type=str, help="path to target image", required=True)
    parser.add_argument('--target-width', type=float, help='target width, in inches', required=True)
    parser.add_argument('--monitor-size', type=float, help='diagonal monitor size in inches', default=24)
    parser.add_argument('--monitor-resolution', type=str, help='monitor res, format: {width}x{height}, ex. 1920x1080', default='1920x1080')
    parser.add_argument('--observer-distance', type=float, help='distance from your eye to the monitor in inches', default=24)
    parser.add_argument('--simulated-distance', type=float, help='target distance to be simulated, in yards', default=7)
    args = parser.parse_args()

    target = cv2.imread(args.target_path, 0)
    target_res_y, target_res_x = target.shape

    target_width_in = args.target_width
    target_height_in = target_width_in / target_res_x * target_res_y

    monitor_res = [int(dim) for dim in args.monitor_resolution.split('x')]
    monitor_width_in = args.monitor_size * monitor_res[0] / (monitor_res[1]**2 + monitor_res[0]**2)**(1/2)
    monitor_height_in = monitor_width_in / monitor_res[0] * monitor_res[1]
    dpi = monitor_res[0] / monitor_width_in 

    # Scaling factor to make the target actual size
    image_scaling_factor = dpi * target_width_in / target_res_x
    # Scaling factor to correct for simulated distance
    distance_scaling_factor = args.observer_distance / (args.simulated_distance * 3 * 12)
    combined_scaling_factor = image_scaling_factor * distance_scaling_factor

    print('Monitor resolution: {}x{}'.format(monitor_res[0], monitor_res[1]))
    print('Monitor dimensions: {:.2f}x{:.2f}", {}" diag'.format(
        monitor_width_in, monitor_height_in, args.monitor_size))
    print('Monitor DPI: {:.2f}'.format(dpi))
    print('Target dimensions: {:.2f}x{:.2f}"'.format(
        target_width_in, target_height_in))
    print('Actual distance: {}"'.format(args.observer_distance))
    print('Simulated distance: {} yards'.format(args.simulated_distance))
    print('Combined Scaling Factor: {:.2f}'.format(combined_scaling_factor))

    resized_target = cv2.resize(target, None, fx=combined_scaling_factor,
            fy=combined_scaling_factor, interpolation = cv2.INTER_AREA)

    new_y, new_x = resized_target.shape
    difference = target_res_x - new_x, target_res_y - new_y
    x_padding, y_padding = int(difference[0] / 2), int(difference[1] / 2)

    padded = cv2.copyMakeBorder(resized_target, top=y_padding, bottom=y_padding,
        left=x_padding, right=x_padding, borderType=cv2.BORDER_CONSTANT, value=255)

    cv2.imshow('{} Yards'.format(args.simulated_distance), padded)
    cv2.waitKey(0)

