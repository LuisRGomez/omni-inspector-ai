
import { GoogleGenAI, Type } from "@google/genai";
import { InspectionMode } from "./types";

export const liveScanObject = async (base64Image: string, mode: InspectionMode) => {
  const ai = new GoogleGenAI({ apiKey: process.env.API_KEY });
  const model = 'gemini-3-flash-preview';
  
  const response = await ai.models.generateContent({
    model,
    contents: { 
      parts: [
        { inlineData: { mimeType: "image/jpeg", data: base64Image.split(',')[1] } }, 
        { text: `Identifica el objeto en esta inspección de ${mode}. Provee nombre y marca regiones de interés (golpes, etiquetas, anomalías).` }
      ] 
    },
    config: {
      responseMimeType: "application/json",
      responseSchema: {
        type: Type.OBJECT,
        properties: {
          objectDetected: { type: Type.STRING },
          regions: {
            type: Type.ARRAY,
            items: {
              type: Type.OBJECT,
              properties: {
                label: { type: Type.STRING },
                box_2d: { type: Type.ARRAY, items: { type: Type.NUMBER } }
              }
            }
          }
        }
      }
    }
  });

  return JSON.parse(response.text || '{}');
};

export const deepForensicAnalysis = async (base64Image: string, mode: InspectionMode) => {
  const ai = new GoogleGenAI({ apiKey: process.env.API_KEY });
  const model = 'gemini-3-pro-preview';

  let prompt = "";
  if (mode === 'food') {
    prompt = `Analiza este alimento perecedero. Determina: 1. Porcentaje exacto de maduración. 2. Presencia de GOLPES, magulladuras o daños físicos. 3. Presencia de moho o patógenos. 4. Días estimados de vida útil. Extrae lote si es visible.`;
  } else if (mode === 'vehicle') {
    prompt = `Analiza este vehículo. Determina: 1. Porcentaje integridad carrocería. 2. Presencia de rayones o abolladuras. 3. Limpieza y mantenimiento. 4. Placa o VIN visible.`;
  } else {
    prompt = `Analiza este contenedor/unidad. Determina: 1. Integridad estructural. 2. Estado de precintos (si visible). 3. Presencia de óxido o agujeros. 4. ID de unidad.`;
  }

  const response = await ai.models.generateContent({
    model,
    contents: { 
      parts: [
        { inlineData: { mimeType: "image/jpeg", data: base64Image.split(',')[1] } }, 
        { text: prompt }
      ] 
    },
    config: {
      responseMimeType: "application/json",
      responseSchema: {
        type: Type.OBJECT,
        properties: {
          objectName: { type: Type.STRING },
          metricA: { type: Type.NUMBER, description: "Maduración (food), Integridad (vehicle/container)" },
          metricB: { type: Type.NUMBER, description: "Calidad (food), Estética (vehicle), Óxido (container)" },
          metricC: { type: Type.NUMBER, description: "Severidad 0-100" },
          shelfLifeDays: { type: Type.NUMBER },
          fraudRisk: { type: Type.NUMBER },
          fraudObservations: { type: Type.STRING },
          regions: {
            type: Type.ARRAY,
            items: {
              type: Type.OBJECT,
              properties: {
                label: { type: Type.STRING },
                box_2d: { type: Type.ARRAY, items: { type: Type.NUMBER } },
                severity: { type: Type.NUMBER }
              }
            }
          },
          extractedData: {
            type: Type.OBJECT,
            properties: {
              lote: { type: Type.STRING },
              id: { type: Type.STRING },
              vencimiento: { type: Type.STRING }
            }
          }
        }
      }
    }
  });

  return JSON.parse(response.text || '{}');
};
