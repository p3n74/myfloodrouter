<?php

?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Map Timeline</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.1/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        .map-thumbnail {
            border: 2px solid transparent;
            cursor: pointer;
            transition: border-color 0.3s;
        }

        .map-thumbnail.active {
            border-color: #007bff; 
        }

        .iframe-container {
            width: 100%;
            height: 500px; 
            border: 2px solid #333; 
        }

        .timeline {
            display: flex;
            gap: 10px;
            overflow-x: auto;
            padding: 10px;
        }

        .row {
            display: flex; 
        }

        #streetListContainer {
            height: 500px; 
            overflow-y: auto; 
            border-left: 2px solid #333;
        }

        .col-md-9, .col-md-3 {
            display: flex;
            flex-direction: column; 
        }
    </style>
</head>
<body>
    <div class="container my-4">
        <div class="row">
            <div class="col-md-9">
                <div id="timeline" class="timeline">
                    <button class="btn btn-outline-primary map-thumbnail" data-map="T307/base.html" data-json="T307/basestreet.json">
                        View Normal Map
                    </button>
                    <button class="btn btn-outline-primary map-thumbnail active" data-map="T307/base.html" data-json="T307/basestreet.json">
                        12:00 am - 2:59 am
                    </button>
                    <button class="btn btn-outline-primary map-thumbnail" data-map="T307/map1.html" data-json="T307/streets1.json">
                        3:00 am - 5:59 am
                    </button>
                    <button class="btn btn-outline-primary map-thumbnail" data-map="T307/base.html" data-json="T307/basestreets.json">
                        6:00 am - 8:59 am
                    </button>
                    <button class="btn btn-outline-primary map-thumbnail" data-map="T307/base.html" data-json="T307/basestreets.json">
                        9:00 am - 11:59 am
                    </button>
                    <button class="btn btn-outline-primary map-thumbnail" data-map="T307/base.html" data-json="T307/basestreets.json">
                        12:00 pm - 2:59 pm
                    </button>
                    <button class="btn btn-outline-primary map-thumbnail" data-map="T307/base.html" data-json="T307/basestreets.json">
                        3:00 pm - 5:59 pm
                    </button>
                    <button class="btn btn-outline-primary map-thumbnail" data-map="T307/base.html" data-json="T307/basestreets.json">
                        6:00 pm - 8:59 pm
                    </button>
                    <button class="btn btn-outline-primary map-thumbnail" data-map="T307/base.html" data-json="T307/basestreets.json">
                        9:00 pm - 11:59 pm
                    </button>
                </div>
                <iframe id="mapViewer" src="map0.html" class="iframe-container mt-3"></iframe>
            </div>
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
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.1/dist/js/bootstrap.bundle.min.js"></script>
    <script>
        async function loadStreets(jsonFile) {
            const streetList = document.getElementById('streetList');
            streetList.innerHTML = '';

            try {
                const response = await fetch(jsonFile);
                if (!response.ok) throw new Error('Failed to fetch streets data.');
                const streets = await response.json();

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

        document.querySelectorAll('.map-thumbnail').forEach(button => {
            button.addEventListener('click', function () {
                document.querySelectorAll('.map-thumbnail').forEach(btn => btn.classList.remove('active'));
                this.classList.add('active');
                
                const mapSrc = this.getAttribute('data-map');
                document.getElementById('mapViewer').src = mapSrc;

                const jsonFile = this.getAttribute('data-json');
                loadStreets(jsonFile);
            });
        });

        loadStreets('streets0.json'); 
    </script>
</body>
</html>