interface MapMarker {
  id: number;
  lat: number;
  lng: number;
  title: string;
  price: string;
  url: string;
  image_url: string;
}

declare global {
  interface Window {
    __uyClickInitMap: (markers: MapMarker[], focusId?: number) => void;
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    ymaps: any;
  }
}

export {};
