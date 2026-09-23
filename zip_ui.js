/* Un .zip hecho en el navegador, sin librerías.

   Lo usan la plantilla de servidor (plantilla_ui.js) y las plantillas de
   modpacks (modpack_ui.js). Va sin comprimir (método «store»): dentro van
   .jar y .txt, y comprimir los .jar otra vez no ahorraría nada.

   window.MTSzip(archivos) → Blob
     archivos: [[nombre, Uint8Array], …] */
(function () {
  const CRC = (() => {
    const t = new Uint32Array(256);
    for (let n = 0; n < 256; n++) {
      let c = n;
      for (let k = 0; k < 8; k++) c = c & 1 ? 0xedb88320 ^ (c >>> 1) : c >>> 1;
      t[n] = c >>> 0;
    }
    return t;
  })();

  function crc32(b) {
    let c = 0xffffffff;
    for (let i = 0; i < b.length; i++) c = CRC[(c ^ b[i]) & 0xff] ^ (c >>> 8);
    return (c ^ 0xffffffff) >>> 0;
  }

  window.MTSzip = function (archivos) {
    const enc = new TextEncoder();
    const partes = [], central = [];
    let off = 0;
    const d = new Date();
    const hora = (d.getHours() << 11) | (d.getMinutes() << 5) | (d.getSeconds() >> 1);
    const dia = ((d.getFullYear() - 1980) << 9) | ((d.getMonth() + 1) << 5) | d.getDate();
    for (const [nombre, datos] of archivos) {
      const n = enc.encode(nombre), crc = crc32(datos), len = datos.length;
      const h = new DataView(new ArrayBuffer(30));
      h.setUint32(0, 0x04034b50, true); h.setUint16(4, 20, true); h.setUint16(6, 0x0800, true);
      h.setUint16(8, 0, true); h.setUint16(10, hora, true); h.setUint16(12, dia, true);
      h.setUint32(14, crc, true); h.setUint32(18, len, true); h.setUint32(22, len, true);
      h.setUint16(26, n.length, true); h.setUint16(28, 0, true);
      partes.push(h.buffer, n, datos);
      const c = new DataView(new ArrayBuffer(46));
      c.setUint32(0, 0x02014b50, true); c.setUint16(4, 20, true); c.setUint16(6, 20, true);
      c.setUint16(8, 0x0800, true); c.setUint16(10, 0, true); c.setUint16(12, hora, true);
      c.setUint16(14, dia, true); c.setUint32(16, crc, true); c.setUint32(20, len, true);
      c.setUint32(24, len, true); c.setUint16(28, n.length, true); c.setUint32(42, off, true);
      central.push(c.buffer, n);
      off += 30 + n.length + len;
    }
    const tam = central.reduce((s, x) => s + (x.byteLength || x.length), 0);
    const e = new DataView(new ArrayBuffer(22));
    e.setUint32(0, 0x06054b50, true); e.setUint16(8, archivos.length, true);
    e.setUint16(10, archivos.length, true); e.setUint32(12, tam, true); e.setUint32(16, off, true);
    return new Blob([...partes, ...central, e.buffer], { type: "application/zip" });
  };

  // Descargar un Blob con nombre, que es lo que hacen las dos páginas después.
  window.MTSdescargar = function (blob, nombre) {
    const a = document.createElement("a");
    a.href = URL.createObjectURL(blob);
    a.download = nombre;
    document.body.appendChild(a); a.click(); a.remove();
    setTimeout(() => URL.revokeObjectURL(a.href), 60000);
  };
})();
