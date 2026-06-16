import React from 'react';
import SoftAurora from './authenticationbg';

const AuthPageLayout = ({ children }) => (
  <div className="min-h-screen flex items-center justify-center p-4 relative overflow-hidden">
    <div className="fixed inset-0 z-0 bg-[#080b14]" aria-hidden="true">
      <SoftAurora
        speed={0.55}
        scale={1.6}
        brightness={0.9}
        color1="#818cf8"
        color2="#8b5cf6"
        noiseFrequency={2.4}
        noiseAmplitude={1.05}
        bandHeight={0.48}
        bandSpread={1.05}
        layerOffset={1.2}
        colorSpeed={0.9}
        enableMouseInteraction={false}
      />
      <div className="absolute inset-0 auth-bg-scrim" />
    </div>

    <div
      className="relative z-10 w-full max-w-md"
      style={{ animation: 'slide-up 0.5s ease forwards' }}
    >
      {children}
    </div>
  </div>
);

export default AuthPageLayout;
