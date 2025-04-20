document.addEventListener('DOMContentLoaded', () => {
    console.log('DOM fully loaded, initializing generate-track script.');
  
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
        const genresInput = document.getElementById('trackGenres')?.value.trim();
        const chartersInput = document.getElementById('trackCharters')?.value.trim();
        const length = parseInt(document.getElementById('trackLength')?.value) || 0;
        const guitarDiff = parseInt(document.getElementById('diffGuitar')?.value) || 0;
        const releaseYear = document.getElementById('trackReleaseYear')?.value || '';
  
        // Validate inputs
        if (length < 0) {
          throw new Error('Length cannot be negative.');
        }
        if (guitarDiff < 0 || guitarDiff > 6) {
          throw new Error('Guitar Difficulty must be between 0 and 6.');
        }
        if (releaseYear && !/^\d{4}$/.test(releaseYear)) {
          throw new Error('Release Year must be a valid 4-digit year.');
        }
  
        const trackData = {
          title: title,
          artist: document.getElementById('trackArtist')?.value.trim() || '',
          preview_start_time: 0, // Default to 0
          release_year: releaseYear,
          source: 'Custom', // Default to Custom
          album: document.getElementById('trackAlbum')?.value.trim() || '',
          loading_phrase: document.getElementById('trackLoadingPhrase')?.value.trim() || '',
          genres: genresInput ? genresInput.split(',').map(g => g.trim()).filter(g => g) : [],
          charters: chartersInput ? chartersInput.split(',').map(c => c.trim()).filter(c => c) : [],
          length: length,
          icon_drums: 'Drum', // Default
          icon_bass: 'Bass', // Default
          icon_guitar: 'Guitar', // Default
          icon_vocals: 'Vocals', // Default
          diff: {
            guitar: guitarDiff,
          },
          midi: document.getElementById('trackMidi')?.value.trim() || '',
          art: 'cover.png',
          stems: {
            drums: ['drums.ogg'], // Default
            bass: 'bass.ogg', // Default
            lead: 'lead.ogg', // Default
            vocals: 'vocals.ogg', // Default
            backing: ['backing.ogg'], // Default
          },
        };
  
        console.log('Track data collected:', trackData);
  
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