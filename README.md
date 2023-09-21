# pygeoapi Docker for KomMonitor 
Docker based setup for KomMonitor related OGC API services. This project samples a process to reproject features up to now.
## Get started
Just run `docker compose up` to start the pygeoapi server. Since there is no custom image up to now, additional Python packages are installed during start up.
You can access the server then via http://localhost:5000/.

You'll find the custom reproject process here: http://localhost:5000/openapi?f=html#/reproject-process/executeReproject-processJob
