
import React, { useState, useRef, useEffect } from 'react';
import { 
  Camera, Upload, Target, Fingerprint, Apple, X, Box, 
  Search, ShieldCheck, RefreshCw, Car, 
  Layers, PlayCircle, CheckCircle2, AlertCircle, Clock
} from 'lucide-react';
import { liveScanObject, deepForensicAnalysis } from './geminiService';
import { InspectionMode, AnalysisStatus } from './types';

const App: React.FC = () => {
  const [mode, setMode] = useState<InspectionMode>('food');
  const [images, setImages] = useState<any[]>([]);
  const [activeIdx, setActiveIdx] = useState(0);
  const [status, setStatus] = useState<AnalysisStatus>(AnalysisStatus.IDLE);
  const [isLive, setIsLive] = useState(false);
  const [coords, setCoords] = useState<{lat: number, lng: number} | null>(null);
  const [liveFeedback, setLiveFeedback] = useState<string>('SCANNING...');
  const [liveRegions, setLiveRegions] = useState<any[]>([]);
  const [activeStream, setActiveStream] = useState<MediaStream | null>(null);
  
  const videoRef = useRef<HTMLVideoElement>(null);
  const scanIntervalRef = useRef<any>(null);

  useEffect(() => {
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        p => setCoords({ lat: p.coords.latitude, lng: p.coords.longitude }),
        () => console.warn("GPS no disponible")
      );
    }
  }, []);

  useEffect(() => {
    if (isLive && videoRef.current && activeStream) {
      videoRef.current.srcObject = activeStream;
      videoRef.current.play().catch(e => console.warn("Video play error:", e));
    }
  }, [isLive, activeStream]);

  const startCamera = async () => {
    try {
      if (activeStream) {
        activeStream.getTracks().forEach(t => t.stop());
      }
      const s = await navigator.mediaDevices.getUserMedia({ 
        video: { facingMode: 'environment', width: { ideal: 1280 } },
        audio: false 
      });
      setActiveStream(s);
      setIsLive(true);
      startLiveScanning(s);
    } catch (e: any) { 
      alert("Error: No se pudo activar la cámara. Revisa los permisos en tu iPhone/Navegador.");
    }
  };

  const stopCamera = () => {
    activeStream?.getTracks().forEach(t => t.stop());
    if (scanIntervalRef.current) clearInterval(scanIntervalRef.current);
    setActiveStream(null);
    setIsLive(false);
  };

  const startLiveScanning = (stream: MediaStream) => {
    if (scanIntervalRef.current) clearInterval(scanIntervalRef.current);
    scanIntervalRef.current = setInterval(async () => {
      if (!videoRef.current || !stream.active) return;
      const canvas = document.createElement('canvas');
      canvas.width = 300; canvas.height = 300;
      canvas.getContext('2d')?.drawImage(videoRef.current, 0, 0, 300, 300);
      try {
        const data = await liveScanObject(canvas.toDataURL('image/jpeg', 0.5), mode);
        if (data.objectDetected) {
          setLiveFeedback(data.objectDetected.toUpperCase());
          setLiveRegions(data.regions || []);
        }
      } catch (e) {}
    }, 2500);
  };

  const addImageToQueue = (base64: string, file?: File) => {
    const timestamp = file ? new Date(file.lastModified).toISOString() : new Date().toISOString();
    const newImg = { 
      url: base64, 
      timestamp,
      coords: coords || undefined,
      status: 'pending', 
      ai: null as any
    };
    setImages(prev => {
      const updated = [...prev, newImg];
      setActiveIdx(updated.length - 1);
      return updated;
    });
  };

  const capture = () => {
    if (!videoRef.current) return;
    const canvas = document.createElement('canvas');
    canvas.width = videoRef.current.videoWidth;
    canvas.height = videoRef.current.videoHeight;
    canvas.getContext('2d')?.drawImage(videoRef.current, 0, 0);
    const base64 = canvas.toDataURL('image/jpeg', 0.8);
    addImageToQueue(base64);
  };

  const runDeepAnalysisBatch = async () => {
    setStatus(AnalysisStatus.DEEP_ANALYZING);
    for (let i = 0; i < images.length; i++) {
      if (images[i].status === 'done') continue;
      setImages(prev => prev.map((img, idx) => idx === i ? { ...img, status: 'analyzing' } : img));
      setActiveIdx(i);
      try {
        const analysis = await deepForensicAnalysis(images[i].url, mode);
        setImages(prev => prev.map((img, idx) => 
          idx === i ? { ...img, ai: analysis, status: 'done' } : img
        ));
      } catch (e) {
        setImages(prev => prev.map((img, idx) => idx === i ? { ...img, status: 'error' } : img));
      }
    }
    setStatus(AnalysisStatus.IDLE);
  };

  const handleFileUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files) {
      Array.from(e.target.files).forEach((f: File) => {
        const r = new FileReader();
        r.onload = ev => addImageToQueue(ev.target?.result as string, f);
        r.readAsDataURL(f);
      });
    }
  };

  const pendingCount = images.filter(img => img.status === 'pending').length;

  return (
    <div className="min-h-screen bg-[#02040a] text-slate-100 font-sans selection:bg-cyan-500/30 overflow-x-hidden">
      
      {/* HEADER HUD */}
      <header className="fixed top-0 inset-x-0 z-[100] bg-black/90 backdrop-blur-xl border-b border-cyan-500/20 p-3 flex flex-col gap-3">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <div className="w-10 h-10 bg-cyan-600 rounded-xl flex items-center justify-center border border-cyan-400/30 shadow-lg shadow-cyan-600/20">
              <Layers className="text-white" size={20} />
            </div>
            <h1 className="text-xs font-black uppercase tracking-tighter text-white">Talos <span className="text-cyan-500">Forensics</span></h1>
          </div>
          <div className="flex gap-2">
            <button onClick={() => document.getElementById('up-talos')?.click()} className="p-2.5 bg-white/5 rounded-xl border border-white/10 text-cyan-400 active:scale-90 transition-transform"><Upload size={18}/></button>
            <input type="file" id="up-talos" className="hidden" multiple onChange={handleFileUpload} />
          </div>
        </div>

        {/* SELECTOR DE MODO TÁCTICO - MEJORADO */}
        <div className="grid grid-cols-3 bg-white/5 rounded-xl p-1 border border-white/10 gap-1">
          {(['food', 'vehicle', 'container'] as InspectionMode[]).map(m => (
            <button 
              key={m} 
              onClick={() => { setMode(m); setIsLive(false); }} 
              className={`flex flex-col items-center justify-center gap-1 py-2 rounded-lg text-[8px] font-black uppercase transition-all ${mode === m ? 'bg-cyan-600 text-white shadow-lg' : 'text-slate-500'}`}
            >
              {m === 'food' ? <Apple size={16}/> : m === 'vehicle' ? <Car size={16}/> : <Box size={16}/>}
              <span>{m === 'food' ? 'Alimento' : m === 'vehicle' ? 'Auto' : 'Logística'}</span>
            </button>
          ))}
        </div>
      </header>

      <main className="pt-40 px-4 max-w-7xl mx-auto grid grid-cols-1 lg:grid-cols-12 gap-6 pb-32">
        
        {/* VISOR */}
        <div className="lg:col-span-8 space-y-4">
          <div className="relative aspect-[4/3] sm:aspect-[16/10] bg-black rounded-[2rem] overflow-hidden border border-cyan-500/30 shadow-2xl ring-1 ring-cyan-500/20">
            {isLive && (
              <div className="absolute top-4 left-4 z-50 bg-black/80 px-4 py-2 rounded-xl border border-cyan-500/40 flex items-center gap-3">
                 <div className="w-2 h-2 bg-cyan-500 rounded-full animate-ping" />
                 <span className="text-[10px] font-black uppercase text-cyan-400">{liveFeedback}</span>
              </div>
            )}

            <div className="w-full h-full">
              {isLive ? (
                <video ref={videoRef} autoPlay playsInline muted className="w-full h-full object-cover" />
              ) : images.length > 0 ? (
                <img src={images[activeIdx]?.url} className="w-full h-full object-cover" />
              ) : (
                <div className="h-full flex flex-col items-center justify-center opacity-20">
                  <Target size={80} className="text-cyan-500 animate-pulse" />
                  <p className="text-[10px] font-black mt-4 uppercase tracking-[0.5em]">Activar Sensor</p>
                </div>
              )}
            </div>

            {/* OVERLAYS */}
            <svg className="absolute inset-0 w-full h-full pointer-events-none z-20" viewBox="0 0 1000 1000" preserveAspectRatio="none">
              {(isLive ? liveRegions : images[activeIdx]?.ai?.regions || []).map((reg: any, i: number) => (
                <g key={i}>
                  <rect x={reg.box_2d[1]} y={reg.box_2d[0]} width={reg.box_2d[3]-reg.box_2d[1]} height={reg.box_2d[2]-reg.box_2d[0]} fill="none" stroke={reg.severity > 30 ? '#f43f5e' : '#06b6d4'} strokeWidth="12" />
                  <foreignObject x={reg.box_2d[1]} y={reg.box_2d[0]-35} width="250" height="35">
                    <div className="px-2 py-0.5 bg-cyan-600 text-[8px] font-black uppercase text-white inline-block">{reg.label}</div>
                  </foreignObject>
                </g>
              ))}
            </svg>
          </div>

          {/* BANDEJA */}
          <div className="bg-black/40 p-4 rounded-[2rem] border border-white/5 flex gap-3 overflow-x-auto no-scrollbar">
             <button onClick={startCamera} className="w-20 h-20 shrink-0 rounded-2xl border-2 border-dashed border-cyan-500/30 flex flex-col items-center justify-center text-cyan-500 bg-cyan-500/5 active:scale-95 transition-transform">
                <Camera size={24}/><span className="text-[8px] font-black uppercase mt-1">Sensor</span>
             </button>
             {images.map((img, i) => (
               <div key={i} className="relative shrink-0">
                  <img src={img.url} onClick={() => { setActiveIdx(i); setIsLive(false); }} className={`w-20 h-20 rounded-2xl object-cover cursor-pointer border-2 ${activeIdx === i && !isLive ? 'border-cyan-500 scale-105' : 'border-transparent opacity-60'}`} />
                  <div className="absolute bottom-1 right-1">
                    {img.status === 'pending' && <Clock size={12} className="text-amber-500" />}
                    {img.status === 'analyzing' && <RefreshCw size={12} className="text-cyan-400 animate-spin" />}
                    {img.status === 'done' && <CheckCircle2 size={12} className="text-emerald-500" />}
                  </div>
               </div>
             ))}
          </div>
        </div>

        {/* DATOS */}
        <div className="lg:col-span-4 space-y-4">
          <div className="bg-[#0b0e14] p-6 rounded-[2.5rem] border border-cyan-500/10 space-y-6 shadow-xl">
            <div className="flex items-center gap-2 text-cyan-400">
              <ShieldCheck size={24} />
              <h2 className="text-lg font-black uppercase">Resultados</h2>
            </div>

            {pendingCount > 0 ? (
              <button onClick={runDeepAnalysisBatch} className="w-full bg-cyan-600 text-white py-4 rounded-xl font-black uppercase tracking-widest active:scale-95">Analizar {pendingCount} Fotos</button>
            ) : images[activeIdx]?.ai ? (
              <div className="space-y-6 animate-in fade-in">
                <div className="grid grid-cols-2 gap-3">
                    <div className="p-4 bg-black/40 rounded-2xl border border-white/5">
                       <span className="text-[8px] font-black text-slate-500 uppercase block mb-1">{mode === 'food' ? 'Maduración' : 'Integridad'}</span>
                       <p className="text-3xl font-black text-white">{images[activeIdx].ai.metricA}%</p>
                    </div>
                    <div className="p-4 bg-black/40 rounded-2xl border border-white/5">
                       <span className="text-[8px] font-black text-slate-500 uppercase block mb-1">{mode === 'food' ? 'Calidad' : 'Estética'}</span>
                       <p className="text-3xl font-black text-cyan-500">{images[activeIdx].ai.metricB}%</p>
                    </div>
                </div>
                <div className="p-4 bg-white/5 rounded-2xl border border-white/10">
                   <span className="text-[9px] font-black text-cyan-500 uppercase block mb-2">Informe Forense</span>
                   <p className="text-xs text-slate-300 italic">"{images[activeIdx].ai.fraudObservations}"</p>
                </div>
              </div>
            ) : (
              <div className="p-10 border-2 border-dashed border-white/5 rounded-3xl flex flex-col items-center justify-center opacity-20 h-48 text-center">
                <Search size={40} /><p className="text-[10px] font-black uppercase mt-2">Captura evidencia para ver detalles</p>
              </div>
            )}
            
            <button onClick={() => { alert("Reporte Exportado."); setImages([]); }} className={`w-full py-4 rounded-xl font-black uppercase text-[10px] tracking-widest ${images.length > 0 ? 'bg-white text-black' : 'bg-white/5 text-slate-600 pointer-events-none'}`}>Generar PDF Pericial</button>
          </div>
        </div>
      </main>

      {/* DISPARADOR */}
      {isLive && (
        <div className="fixed bottom-10 inset-x-0 flex justify-center gap-8 z-[200]">
           <button onClick={stopCamera} className="bg-rose-600/20 text-rose-500 p-6 rounded-full border border-rose-600/30 backdrop-blur-xl"><X size={28}/></button>
           <button onClick={capture} className="bg-white w-20 h-20 rounded-full flex items-center justify-center border-8 border-black shadow-2xl active:scale-90 transition-all">
              <div className="w-10 h-10 bg-cyan-600 rounded-full" />
           </button>
        </div>
      )}

      {/* CARGA */}
      {status === AnalysisStatus.DEEP_ANALYZING && (
        <div className="fixed inset-0 bg-black/95 z-[600] flex flex-col items-center justify-center p-10">
           <div className="relative w-48 h-48 mb-8 flex items-center justify-center">
              <div className="absolute inset-0 border-[10px] border-white/5 border-t-cyan-500 rounded-full animate-spin" />
              <Fingerprint size={60} className="text-cyan-500 animate-pulse" />
           </div>
           <h4 className="text-2xl font-black text-white uppercase tracking-tighter">Analizando...</h4>
        </div>
      )}

      <style>{`.no-scrollbar::-webkit-scrollbar { display: none; }`}</style>
    </div>
  );
};

export default App;
