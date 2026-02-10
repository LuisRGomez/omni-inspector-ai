
export type InspectionMode = 'food' | 'vehicle' | 'container';

export interface ManualAnnotation {
  x: number;
  y: number;
  label: string;
  note?: string;
}

export interface DetectionRegion {
  label: string;
  box_2d: [number, number, number, number];
  severity: number;
  type: string;
}

export interface ImageMetadata {
  url: string;
  name: string;
  regions: DetectionRegion[];
  manualMarks: ManualAnnotation[];
  timestamp: string; // ISO String
  coords?: { lat: number, lng: number };
  fileData?: {
    lastModified: number;
    size: number;
    type: string;
  };
  aiAnalysis?: {
    objectName: string;
    confidence: number;
    fraudScore: number;
    observations: string;
    detectedData: {
      lote?: string;
      vencimiento?: string;
      temperatura?: string;
    };
  };
}

export interface InspectionReport {
  id: string;
  status: 'draft' | 'certified';
  context: {
    fechaHora: string;
    lugar: string;
    solicitante: string;
    intervinientes: string;
    coords?: { lat: number, lng: number };
  };
  logistics: {
    unidadId: string;
    precintoId: string;
    precintoStatus: 'intacto' | 'roto' | 'ausente';
    setPoint: string;
    displayTemp: string;
    ventilas: 'abiertas' | 'cerradas';
  };
  goods: {
    producto: string;
    lote: string;
    cantidadDeclarada: string;
    cantidadReal: string;
  };
  physical: {
    temperaturasPulpa: number[];
    organoleptic: { olor: string; color: string; textura: string; };
    mohoPercentage: number;
  };
  valuation: {
    sanoPercentage: number;
    recuperoPercentage: number;
    perdidaPercentage: number;
    valorMercado: string;
    recomendacion: string;
  };
  audit: {
    metadataInconsistencies: string[];
    fraudAlerts: string[];
    objectMismatch?: string;
  };
}

export enum AnalysisStatus {
  IDLE = 'IDLE',
  LIVE_SCANNING = 'LIVE_SCANNING',
  DEEP_ANALYZING = 'DEEP_ANALYZING',
  WIZARD = 'WIZARD',
  SUCCESS = 'SUCCESS'
}
