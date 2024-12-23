use ffmpeg_next as ffmpeg;
use std::process::Command;

fn main() -> Result<(), ffmpeg::Error> {
    ffmpeg::init()?;

    let input_file = "input.mp4"; // Replace with your input file
    let output_prefix = "output";

    // 1. Analyze the video for scene changes using FFmpeg's scene detection filter.
    let scene_data = Command::new("ffprobe")
        .args(
            &[
                "-f",
                "lavutils",
                "-i",
                input_file,
                "-show_frames",
                "-show_entries",
                "frame=pts_time,media_type",
                "-of",
                "csv=p=0",
                "-vf",
                "select='gt(scene,0.4)'", // Adjust the threshold (0.4) as needed
                "-print_format",
                "csv=print_section=0",
            ]
        )
        .output()
        .expect("Failed to execute ffprobe");

    let scene_output = String::from_utf8_lossy(&scene_data.stdout);

    // 2. Parse the output of ffprobe to get the timestamps of scene changes.
    let scene_times: Vec<f64> = scene_output
        .lines()
        .filter(|line| line.contains("video")) // filter out audio lines
        .map(|line| {
            let parts: Vec<&str> = line.split(',').collect();
            parts[0].parse().unwrap_or(0.0)
        })
        .collect();

    // 3. Split the video using FFmpeg based on the detected scene change timestamps.
    for i in 0..scene_times.len() {
        let start_time = if i == 0 { 0.0 } else { scene_times[i - 1] };
        let end_time = scene_times[i];
        let duration = end_time - start_time;

        let output_file = format!("{}_{}.mp4", output_prefix, i);

        Command::new("ffmpeg")
            .args(
                &[
                    "-i",
                    input_file,
                    "-ss",
                    &start_time.to_string(),
                    "-t",
                    &duration.to_string(),
                    "-c:v",
                    "copy", // Copy video codec
                    "-c:a",
                    "copy", // Copy audio codec
                    &output_file,
                ]
            )
            .status()
            .expect("Failed to execute ffmpeg");

        println!("Created {}", output_file);
    }

    Ok(())
}
