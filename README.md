# SID-SLAM

## Run Comparison

bash```
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
