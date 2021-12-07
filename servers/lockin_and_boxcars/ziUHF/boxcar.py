# Copyright 2016 Zurich Instruments AG

"""
Zurich Instruments LabOne Python API Example
Demonstrate how to connect to a Zurich Instruments UHF Lock-in Amplifier and
obtain output from the Input PWA and Boxcar using ziDAQServer's poll() command.
Connect to a Zurich Instruments UHF Lock-in Amplifier and
obtain Input PWA and Boxcar data via ziDAQServer's synchronous poll command.
Requirements:
    * LabOne Version >= 21.02
    * Instruments:
        1 x UHF Instruments with the BOX option enabled.
Usage:
    example_boxcar.py [options] <device_id>
    example_boxcar.py -h | --help
Arguments:
    <device_id>  The ID of the device to run the example with. [device_type: UHF(BOX)]
Options:
    -h --help              Show this screen.
    -s --server_host IP    Hostname or IP address of the dataserver [default: localhost]
    -p --server_port PORT  Port number of the data server [default: 8004]
    --no-plot              Hide plot of the recorded data.
Returns:
    sample  A dictionary containing the boxcar sample.
Raises:
    Exception     If the specified device does not match the requirements.
    RuntimeError  If the device is not "discoverable" from the API.
See the LabOne Programming Manual for further help:
https://docs.zhinst.com/labone_programming_manual/
"""

import time
import numpy as np
import zhinst.utils
import matplotlib.pyplot as plt


def run_example(
    device_id: str,
    server_host: str = "localhost",
    server_port: int = 8004,
    plot: bool = True,
):
    """run the example."""

    apilevel_example = 6  # The API level supported by this example.
    # Call a zhinst utility function that returns:
    # - an API session `daq` in order to communicate with devices via the data server.
    # - the device ID string that specifies the device branch in the server's node hierarchy.
    # - the device's discovery properties.
    (daq, device, props) = zhinst.utils.create_api_session(
        device_id, apilevel_example, server_host=server_host, server_port=server_port
    )
    zhinst.utils.api_server_version_check(daq)

    # Create a base configuration: Disable all available outputs, awgs, demods, scopes,...
    zhinst.utils.disable_everything(daq, device)

    # Now configure the instrument for this experiment. The following channels
    # and indices work on all device configurations. The values below may be
    # changed if the instrument has multiple input/output channels and/or either
    # the Multifrequency or Multidemodulator options installed.
    out_channel = 0
    out_mixer_channel = zhinst.utils.default_output_mixer_channel(props)
    in_channel = 0
    osc_index = 0
    frequency = 400e3
    boxcar_index = 0
    inputpwa_index = 0
    amplitude = 0.5
    frequency = 9.11e6
    windowstart = 75  # boxcar windowstart [degrees]
    windowsize = 3e-9  # boxcar windowsize [seconds]
    periods_vals = np.logspace(0, 9, 10, base=2)
    exp_setting = [
        ["/%s/sigins/%d/imp50" % (device, in_channel), 1],
        ["/%s/sigins/%d/ac" % (device, in_channel), 0],
        ["/%s/sigins/%d/range" % (device, in_channel), 2 * amplitude],
        ["/%s/inputpwas/%d/oscselect" % (device, inputpwa_index), osc_index],
        ["/%s/inputpwas/%d/inputselect" % (device, inputpwa_index), in_channel],
        ["/%s/inputpwas/%d/mode" % (device, inputpwa_index), 1],
        ["/%s/inputpwas/%d/shift" % (device, inputpwa_index), 0.0],
        ["/%s/inputpwas/%d/harmonic" % (device, inputpwa_index), 1],
        ["/%s/inputpwas/%d/enable" % (device, inputpwa_index), 1],
        ["/%s/boxcars/%d/oscselect" % (device, boxcar_index), osc_index],
        ["/%s/boxcars/%d/inputselect" % (device, boxcar_index), in_channel],
        ["/%s/boxcars/%d/windowstart" % (device, boxcar_index), windowstart],
        ["/%s/boxcars/%d/windowsize" % (device, boxcar_index), windowsize],
        ["/%s/boxcars/%d/limitrate" % (device, boxcar_index), 1e3],
        ["/%s/boxcars/%d/periods" % (device, boxcar_index), periods_vals[0]],
        ["/%s/boxcars/%d/enable" % (device, boxcar_index), 1],
        ["/%s/oscs/%d/freq" % (device, osc_index), frequency],
        ["/%s/sigouts/%d/on" % (device, out_channel), 1],
        ["/%s/sigouts/%d/enables/%d" % (device, out_channel, out_mixer_channel), 1],
        ["/%s/sigouts/%d/range" % (device, out_channel), 1],
        [
            "/%s/sigouts/%d/amplitudes/%d" % (device, out_channel, out_mixer_channel),
            amplitude,
        ],
    ]
    daq.set(exp_setting)

    # Wait for boxcar output to settle
    time.sleep(periods_vals[0] / frequency)

    # Perform a global synchronisation between the device and the data server:
    # Ensure that the settings have taken effect on the device before issuing
    # the poll().
    daq.sync()

    # Get the values that were actually set on the device
    frequency_set = daq.getDouble("/%s/oscs/%d/freq" % (device, osc_index))
    windowstart_set = daq.getDouble(
        "/%s/boxcars/%d/windowstart" % (device, boxcar_index)
    )
    windowsize_set = daq.getDouble("/%s/boxcars/%d/windowsize" % (device, boxcar_index))

    # Subscribe to the nodes we would like to record data from
    boxcar_sample_path = "/%s/boxcars/%d/sample" % (device, boxcar_index)
    boxcar_periods_path = "/%s/boxcars/%d/periods" % (device, boxcar_index)
    inputpwa_wave_path = "/%s/inputpwas/%d/wave" % (device, inputpwa_index)
    daq.subscribe([boxcar_sample_path, boxcar_periods_path, inputpwa_wave_path])
    # We use getAsEvent() to ensure we obtain the first ``periods`` value; if
    # its value didn't change, the server won't report the first value.
    daq.getAsEvent(boxcar_periods_path)

    for periods in periods_vals:
        time.sleep(0.5)
        daq.setInt(boxcar_periods_path, int(periods))

    # Poll the data
    poll_length = 0.1  # [s]
    poll_timeout = 500  # [ms]
    poll_flags = 0
    poll_return_flat_dict = True
    data = daq.poll(poll_length, poll_timeout, poll_flags, poll_return_flat_dict)

    # Unsubscribe from all paths
    daq.unsubscribe("*")

    # Check the dictionary returned by poll contains the subscribed data. The
    # data returned is a dictionary with keys corresponding to the recorded
    # data's path in the node hierarchy
    assert (
        data
    ), "poll returned an empty data dictionary, did you subscribe to any paths?"
    assert boxcar_sample_path in data, (
        "data dictionary has no key '%s'" % boxcar_sample_path
    )
    assert boxcar_periods_path in data, (
        "data dictionary has no key '%s'" % boxcar_periods_path
    )
    assert inputpwa_wave_path in data, (
        "data dictionary has no key '%s'" % inputpwa_wave_path
    )

    sample = data[boxcar_sample_path]

    # When using API Level 4 (or higher) poll() returns both the 'value' and
    # 'timestamp' of the node. These are two vectors of the same length;
    # which consist of (timestamp, value) pairs.
    boxcar_value = sample["value"]
    boxcar_timestamp = sample["timestamp"]
    boxcar_periods_value = data[boxcar_periods_path]["value"]
    boxcar_periods_timestamp = data[boxcar_periods_path]["timestamp"]

    print(f"Measured average boxcar amplitude is {np.mean(boxcar_value):.5e} V.")

    if plot:
        # get the sample rate of the device's ADCs
        clockbase = float(daq.getInt("/%s/clockbase" % device))
        # convert timestamps from ticks to seconds via clockbase
        boxcar_t = (boxcar_timestamp - boxcar_timestamp[0]) / clockbase
        boxcar_periods_t = (
            boxcar_periods_timestamp - boxcar_periods_timestamp[0]
        ) / clockbase
        boxcar_periods_t[0] = boxcar_t[0]
        # Create plot
        _, ax1 = plt.subplots()
        ax2 = ax1.twinx()

        ax1.grid(True)
        ax1.plot(boxcar_t, boxcar_value, label="boxcar output")
        ax1.set_xlabel("Time (s)")

        ax2.step(
            np.append(boxcar_periods_t, boxcar_t[-1]),
            np.append(boxcar_periods_value, boxcar_periods_value[-1]),
            "-r",
            label="Averaging periods",
        )
        ax2.set_yscale("log")
        ax1.set_xlim(
            min(boxcar_t[0], boxcar_periods_t[0]),
            max(boxcar_t[-1], boxcar_periods_t[-1]),
        )
        ax2.legend(loc=1)
        ax1.set_title(
            "Boxcar output: The effect of averaging\nperiods on the boxcar value."
        )
        ax1.legend(loc=4)
        ax1.set_ylabel("Boxcar value (V)")
        ax2.set_ylabel("Number of Averaging Periods")

        _, axis = plt.subplots()
        axis.grid(True)
        pwa_wave = data[inputpwa_wave_path][-1]
        pwa_wave["binphase"] = pwa_wave["binphase"] * 360 / (2 * np.pi)
        axis.axhline(0, color="k")
        # The inputpwa waveform is stored in 'x', currently 'y' is unused.
        axis.plot(pwa_wave["binphase"], pwa_wave["x"])
        windowsize_set_degrees = 360 * frequency_set * windowsize_set
        phase_window = (pwa_wave["binphase"] >= windowstart_set) & (
            pwa_wave["binphase"] <= windowstart_set + windowsize_set_degrees
        )
        axis.fill_between(
            pwa_wave["binphase"], 0, pwa_wave["x"], where=phase_window, alpha=0.5
        )
        axis.set_xlim(0, 360)
        title = "Input PWA waveform, the shaded region shows the portion\n of the waveform the \
            boxcar is integrating."
        axis.set_title(title)
        axis.set_xlabel("Phase (degrees)")
        axis.set_ylabel("Amplitude (V)")

        plt.show()

    return sample


if __name__ == "__main__":
    import sys
    from pathlib import Path

    cli_util_path = Path(__file__).resolve().parent / "../../utils/python"
    sys.path.insert(0, str(cli_util_path))
    cli_utils = __import__("cli_utils")
    cli_utils.run_commandline(run_example, __doc__)
    sys.path.remove(str(cli_util_path))