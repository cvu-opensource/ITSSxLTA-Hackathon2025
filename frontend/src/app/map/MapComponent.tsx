"use client";

import {
  GoogleMap,
  OverlayView,
  useLoadScript,
} from "@react-google-maps/api";
import { useState, useCallback } from "react";
import {
  Popover,
  PopoverTrigger,
  PopoverContent,
} from "@/components/ui/popover";
import { rawMarkers } from "@/data/markers";
import { FaLocationArrow } from "react-icons/fa"; 

const mapContainerStyle = {
  width: "100%",
  height: "calc(100vh - 100px)", // Adjust to fit your layout
};

const center = { lat: 1.3521, lng: 103.8198 }; // Singapore

export default function MapComponent() {
  const { isLoaded, loadError } = useLoadScript({
    googleMapsApiKey: process.env.NEXT_PUBLIC_GOOGLE_MAPS_API_KEY || "",
  });

  const [activeMarker, setActiveMarker] = useState<number | null>(null);

  const onLoad = useCallback((map: google.maps.Map) => {}, []);

  const markers = Object.entries(rawMarkers).map(([id, data]) => ({
    id: Number(id),
    position: {
      lat: data.camera_data.lat,
      lng: data.camera_data.long,
    },
    location: data.camera_data.description,
    degrees: data.camera_data.angle,
    status: data.traffic_data.status,
    vehiclesDetected: Math.round(data.traffic_data.num_vehicles.average),
    carSpeed: `${(data.traffic_data.pixel_speed.relative * 50).toFixed(1)} km/h`,
    lastUpdated: new Date(data.image_data.datetime).toLocaleString(),
    image: data.image_data.image_link,
    action: data.image_data.accident_detected ? "⚠️ Accident Detected" : null,
    pixelSpeed: data.traffic_data.pixel_speed.relative.toFixed(2),
    trafficDensity: data.traffic_data.traffic_density.relative.toFixed(2),
  }));

  if (loadError) return <p>Error loading map</p>;
  if (!isLoaded) return <p>Loading map...</p>;

  return (
    <div className="relative">
      <GoogleMap
        mapContainerStyle={mapContainerStyle}
        center={center}
        zoom={12}
        onLoad={onLoad}
      >
        {markers.map((marker) => (
          <div key={marker.id}>
            {/* 🟢 Custom React Icon Marker */}
            <OverlayView
              position={marker.position}
              mapPaneName={OverlayView.OVERLAY_MOUSE_TARGET}
            >
              <div className="relative flex items-center justify-center">
                {/* Pulse Animation */}
                <span
                  className={`
                    absolute inline-flex h-6 w-6 rounded-full animate-ping opacity-75
                    ${marker.status === "congested" || marker.action ? "bg-red-400" : "bg-green-400"}
                  `}
                />
                {/* React Icon */}
                <div
                  className="z-20 flex items-center justify-center w-8 h-8"
                  onClick={() => setActiveMarker(marker.id)}
                  style={{ transform: `rotate(${marker.degrees - 45}deg)` }}
                >
                  <FaLocationArrow
                    className={`
                      text-3xl transition-transform duration-200
                      ${marker.status === "congested" || marker.action ? "text-red-600" : "text-green-500"}
                      hover:scale-125 active:scale-90 cursor-pointer
                    `}
                  />
                </div>
              </div>
            </OverlayView>

            {/* 🟡 Popover */}
            {activeMarker === marker.id && (
              <OverlayView
                position={marker.position}
                mapPaneName={OverlayView.OVERLAY_MOUSE_TARGET}
                getPixelPositionOffset={() => ({ x: -20, y: -45 })}
              >
                <div className="relative">
                  <Popover open={true} onOpenChange={() => setActiveMarker(null)}>
                    <PopoverTrigger asChild>
                      <button className="w-0 h-0 opacity-0 absolute" />
                    </PopoverTrigger>
                    <PopoverContent
                      className={`p-4 rounded-lg shadow-lg w-72 transition-colors ${
                        marker.status === "congested" || marker.action
                          ? "bg-red-900 text-white"
                          : "bg-gray-900 text-white"
                      }`}
                    >
                      <p className="font-bold text-lg">{marker.location}</p>
                      <p className="text-sm text-gray-300">
                        Last Updated: {marker.lastUpdated}
                      </p>
                      <p className="mt-1">
                        Vehicles Detected: <span className="font-bold">{marker.vehiclesDetected}</span>
                      </p>
                      <p className="mt-1">
                        Car Speed: <span className="font-bold">{marker.carSpeed}</span>
                      </p>
                      <p className="mt-1">
                        Pixel Speed:{" "}
                        <span className="font-bold">{marker.pixelSpeed}</span>
                      </p>
                      <p className="mt-1">
                        Traffic Density:{" "}
                        <span className="font-bold">{marker.trafficDensity}</span>
                      </p>
                      {marker.image && (
                        <img
                          src={marker.image}
                          alt="Live camera feed"
                          className="mt-3 w-full h-auto rounded"
                        />
                      )}
                      {marker.action && (
                        <p className="mt-2 text-red-300">
                          ⚠️ <strong>Recommended Actions:</strong> {marker.action}
                        </p>
                      )}
                    </PopoverContent>
                  </Popover>
                </div>
              </OverlayView>
            )}
          </div>
        ))}
      </GoogleMap>
    </div>
  );
}
