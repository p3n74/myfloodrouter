<?php
// Your PHP code can go here if needed
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Map Timeline</title>
    <!-- Bootstrap CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.1/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        .map-thumbnail {
            border: 2px solid transparent;
            cursor: pointer;
            transition: border-color 0.3s;
        }

        .map-thumbnail.active {
            border-color: #007bff; /* Highlight color */
        }

        .iframe-container {
            width: 100%;
            height: 500px; /* Fixed height for the map */
            border: 2px solid #333; /* Border for the map */
        }

        .timeline {
            display: flex;
            gap: 10px;
            overflow-x: auto;
            padding: 10px;
        }

        /* Adjust the height of the street list to match the map */
        #streetListContainer {
            height: 500px; /* Match the height of the map */
            overflow-y: auto; /* Enable vertical scrolling */
        }
    </style>
</head>
<body>
    <div class="container my-4">
        <div class="row">
            <!-- Timeline -->
            <div class="col-md-9">
                <div id="timeline" class="timeline">
                    <!-- Buttons for each map -->
                    <button class="btn btn-outline-primary map-thumbnail active" data-map="map0.html" data-json="streets0.json">
                        Now
                    </button>
                    <button class="btn btn-outline-primary map-thumbnail" data-map="map1.html" data-json="streets1.json">
                        +3h
                    </button>
                    <button class="btn btn-outline-primary map-thumbnail" data-map="map2.html" data-json="streets2.json">
                        +6h
                    </button>
                    <button class="btn btn-outline-primary map-thumbnail" data-map="map3.html" data-json="streets3.json">
                        +9h
                    </button>
                    <button class="btn btn-outline-primary map-thumbnail" data-map="map4.html" data-json="streets4.json">
                        +12h
                    </button>
                    <button class="btn btn-outline-primary map-thumbnail" data-map="map5.html" data-json="streets5.json">
                        +15h
                    </button>
                    <button class="btn btn-outline-primary map-thumbnail" data-map="map6.html" data-json="streets6.json">
                        +18h
                    </button>
                    <button class="btn btn-outline-primary map-thumbnail" data-map="map7.html" data-json="streets7.json">
                        +21h
                    </button>
                </div>
                <!-- Map Viewer -->
                <iframe id="mapViewer" src="map0.html" class="iframe-container mt-3"></iframe>
            </div>
            <!-- Street List -->
            <div class="col-md-3">
                <h4>Street List</h4>
                <div id="streetListContainer">
                    <table class="table table-bordered table-striped">
                        <thead>
                            <tr>
                                <th>#</th>
                                <th>Street Name</th>
                            </tr>
                        </thead>
                        <tbody id="streetList">
                            <!-- Streets will be dynamically loaded here -->
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    </div>

    <!-- Bootstrap JS -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.1/dist/js/bootstrap.bundle.min.js"></script>
    <script>
        // Function to load the JSON file and populate the street list
        async function loadStreets(jsonFile) {
            const streetList = document.getElementById('streetList');
            streetList.innerHTML = ''; // Clear existing data

            try {
                const response = await fetch(jsonFile);
                if (!response.ok) throw new Error('Failed to fetch streets data.');
                const streets = await response.json();

                // Populate the street list table
                streets.forEach((street, index) => {
                    const row = document.createElement('tr');
                    row.innerHTML = `<td>${index + 1}</td><td>${street}</td>`;
                    streetList.appendChild(row);
                });
            } catch (error) {
                console.error(error);
                streetList.innerHTML = '<tr><td colspan="2">Error loading streets.</td></tr>';
            }
        }

        // Event listeners for map buttons
        document.querySelectorAll('.map-thumbnail').forEach(button => {
            button.addEventListener('click', function () {
                // Highlight the selected map
                document.querySelectorAll('.map-thumbnail').forEach(btn => btn.classList.remove('active'));
                this.classList.add('active');
                
                // Load the corresponding map in the iframe
                const mapSrc = this.getAttribute('data-map');
                document.getElementById('mapViewer').src = mapSrc;

                // Load the corresponding streets JSON
                const jsonFile = this.getAttribute('data-json');
                loadStreets(jsonFile);
            });
        });

        // Initial load
        loadStreets('streets0.json'); // Load the streets for the first map
    </script>
</body>
</html>