document.addEventListener('DOMContentLoaded', () => {
  console.log('DOM fully loaded, initializing generate-preview script.');

  const downloadJsonButton = document.getElementById('downloadJson');

  // Check if button exists
  if (!downloadJsonButton) {
    console.error('Download JSON button not found. Ensure the button has id="downloadJson" in the HTML.');
    return;
  }

  console.log('Download JSON button found, attaching event listener.');

  downloadJsonButton.addEventListener('click', () => {
    console.log('Download JSON button clicked.');

    try {
      // Collect form data
      const title = document.getElementById('trackTitle')?.value.trim() || '';
      const completePercent = parseInt(document.getElementById('trackComplete')?.value) || 100;
      if (completePercent < 0 || completePercent > 100) {
        throw new Error('Completion percentage must be between 0 and 100.');
      }

      const trackData = {
        title: title,
        artist: document.getElementById('trackArtist')?.value.trim() || '',
        releaseYear: parseInt(document.getElementById('trackReleaseYear')?.value) || 0,
        cover: document.getElementById('trackCover')?.value.trim() || '',
        bpm: parseInt(document.getElementById('trackBpm')?.value) || 0,
        duration: document.getElementById('trackDuration')?.value.trim() || '0m 0s',
        difficulties: {
          vocals: parseInt(document.getElementById('diffVocals')?.value) || -1,
          guitar: parseInt(document.getElementById('diffGuitar')?.value) || -1,
          bass: parseInt(document.getElementById('diffBass')?.value) || -1,
          drums: parseInt(document.getElementById('diffDrums')?.value) || -1,
          'plastic-bass': parseInt(document.getElementById('diffPlasticBass')?.value) || -1,
          'plastic-drums': parseInt(document.getElementById('diffPlasticDrums')?.value) || -1,
          'plastic-guitar': parseInt(document.getElementById('diffPlasticGuitar')?.value) || -1,
        },
        createdAt: new Date().toISOString(),
        lastFeatured: new Date().toLocaleString('en-US', {
          month: 'numeric',
          day: 'numeric',
          year: 'numeric',
          hour: 'numeric',
          minute: 'numeric',
          second: 'numeric',
          hour12: true,
        }),
        complete: `${completePercent}% Complete`,
        videoUrl: document.getElementById('trackVideoUrl')?.value.trim() || '',
        videoPosition: parseInt(document.getElementById('trackVideoPosition')?.value) || 20,
        download: document.getElementById('trackDownload')?.value.trim() || '',
        spotify: document.getElementById('trackSpotify')?.value.trim() || '',
        previewUrl: document.getElementById('trackPreviewUrl')?.value.trim() || '',
        featured: document.getElementById('trackFeatured')?.checked || false,
        new: document.getElementById('trackNew')?.checked || false,
        youtubeLinks: {
          vocals: document.getElementById('youtubeVocals')?.value.trim() || '',
          lead: document.getElementById('youtubeLead')?.value.trim() || '',
          bass: document.getElementById('youtubeBass')?.value.trim() || '',
          drums: document.getElementById('youtubeDrums')?.value.trim() || '',
        },
      };

      console.log('Track data collected:', trackData);

      // Validate duration format if provided
      if (trackData.duration && !/^\d+m \d+s$/.test(trackData.duration)) {
        alert('Duration must be in Xm Ys format (e.g., 2m 21s) if provided.');
        console.error('Invalid duration format:', trackData.duration);
        return;
      }

      // Validate difficulty values
      for (const [key, value] of Object.entries(trackData.difficulties)) {
        if (value < -1 || value > 6) {
          throw new Error(`Difficulty for ${key} must be between -1 and 6.`);
        }
      }

      // Generate JSON
      const jsonString = JSON.stringify(trackData, null, 2);
      console.log('Generated JSON:', jsonString);

      // Download JSON as file named info.json
      const blob = new Blob([jsonString], { type: 'application/json' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = 'info.json';
      console.log('Initiating download for file: info.json');
      a.click();
      URL.revokeObjectURL(url);
      console.log('Download triggered successfully.');

      // Navigate to index.html
      setTimeout(() => {
        window.location.href = 'index.html';
      }, 500); // Delay to ensure download completes
    } catch (error) {
      console.error('Error generating or downloading JSON:', error.message);
      alert(`Failed to download JSON: ${error.message}`);
    }
  });
});