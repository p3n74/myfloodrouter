<?php
$route = isset($_GET['route']) ? $_GET['route'] : '';
$routeInfo = [
    'A' => ['name' => 'Route A'],
    'B' => ['name' => 'Route B'],
    'C' => ['name' => 'Route C'],
];

// Read the JSON file
$jsonContent = file_get_contents('t307_route_streets.json');
$routeData = json_decode($jsonContent, true);
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Flood Router 2.0 - <?php echo $routeInfo[$route]['name']; ?></title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        #map-container {
            width: 100%;
            height: 600px;
            border: 1px solid #ddd;
        }
        #map-container iframe {
            width: 100%;
            height: 100%;
            border: none;
        }
        .street-item {
            cursor: pointer;
        }
        .street-item:hover {
            background-color: #f8f9fa;
        }
    </style>
</head>
<body>
    <div class="container-fluid mt-3">
        <h1 class="mb-4"><?php echo $routeInfo[$route]['name']; ?></h1>
        <div class="row">
            <div class="col-md-9">
                <div id="map-container">
                    <iframe src="t307_jeepney_route_with_streets.html" id="map-frame"></iframe>
                </div>
            </div>
            <div class="col-md-3">
                <div class="card">
                    <div class="card-body">
                        <h5 class="card-title">Route Information</h5>
                        <h6 class="card-subtitle mb-2 text-muted">Streets in this route:</h6>
                        <ol class="list-group list-group-numbered">
                            <?php 
                            // Assuming the 'route' key contains the route's relevant streets
                            // Loop through each street and display its name
                            foreach ($routeData as $streetData): 
                                $streetName = $streetData['street_name']; 
                            ?>
                                <li class="list-group-item street-item" data-street-name="<?php echo htmlspecialchars($streetName); ?>">
                                    <?php echo htmlspecialchars($streetName); ?>
                                </li>
                            <?php endforeach; ?>
                        </ol>
                        <a href="index.php" class="btn btn-primary mt-3">Back to Home</a>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/js/bootstrap.bundle.min.js"></script>
    <script>
        document.addEventListener('DOMContentLoaded', function() {
            const streetItems = document.querySelectorAll('.street-item');
            const mapFrame = document.getElementById('map-frame');

            streetItems.forEach(item => {
                item.addEventListener('click', function() {
                    const streetName = this.getAttribute('data-street-name');
                    // Assuming map interaction with the frame based on street name
                    mapFrame.contentWindow.postMessage({
                        action: 'highlightStreet',
                        streetName: streetName
                    }, '*');
                });
            });
        });
    </script>
</body>
</html>
