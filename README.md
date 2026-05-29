# SID-SLAM

## Run Algorithm 

```bash
/home/tom/Documents/PhD/unseen_slam/comparisons/SID-SLAM/Examples/RGB-D/TUM/rgbdTUM /home/tom/Documents/PhD/unseen_slam/results/comparison_20260529_150447_2cbac00/rgbd_dataset_freiburg2_pioneer_slam/SID-SLAM/sequence_config /home/tom/Documents/PhD/unseen_slam/results/comparison_20260529_150447_2cbac00/rgbd_dataset_freiburg2_pioneer_slam/SID-SLAM/systemSettings.headless.yaml 0 /home/tom/Documents/PhD/unseen_slam/results/comparison_20260529_150447_2cbac00/rgbd_dataset_freiburg2_pioneer_slam/SID-SLAM /home/tom/Documents/PhD/unseen_slam/datasets
```

to run it with built-in waits enabled: 
```bash
SID_SLAM_ENABLE_WAITS=1 <command>
```

It can also be stopped in the Relocalization mode: 
```bash
SID_SLAM_MAX_RELOCALIZATION_FRAMES=10 <your rgbdTUM command>
```
## Run Comparison

```bash
python3 comparisons/SID-SLAM/run_comparison.py \
  --dataset datasets/rgbd_dataset_freiburg2_pioneer_slam \
  --output /tmp/sid_slam_run \
  --repo-root "$PWD" \
  --algorithm-dir comparisons/SID-SLAM \
  --run-root /tmp/sid_slam_run
```
Implements SID-SLAM: Semi-Direct Information-Driven RGB-D SLAM

Reference:
```
@ARTICLE{10058038,
  author={Fontan, Alejandro and Giubilato, Riccardo and Maza, Laura Oliva and Civera, Javier and Triebel, Rudolph},
  journal={IEEE Robotics and Automation Letters}, 
  title={SID-SLAM: Semi-Direct Information-Driven RGB-D SLAM}, 
  year={2023},
  volume={8},
  number={10},
  pages={6387-6394},
  keywords={Simultaneous localization and mapping;Entropy;Cameras;Optimization;Jacobian matrices;Robustness;Pipelines;Localization;SLAM},
  doi={10.1109/LRA.2023.3251722}}
```
