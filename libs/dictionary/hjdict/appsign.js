var n = {
    rotl: function(t, e) {
        return t << e | t >>> 32 - e
    },
    rotr: function(t, e) {
        return t << 32 - e | t >>> e
    },
    endian: function(t) {
        if (t.constructor == Number) return 16711935 & n.rotl(t, 8) | 4278255360 & n.rotl(t, 24);
        for (var e = 0; e < t.length; e++) t[e] = n.endian(t[e]);
        return t
    },
    randomBytes: function(t) {
        for (var e = []; t > 0; t--) e.push(Math.floor(256 * Math.random()));
        return e
    },
    bytesToWords: function(t) {
        for (var e = [], n = 0, i = 0; n < t.length; n++, i += 8) e[i >>> 5] |= t[n] << 24 - i % 32;
        return e
    },
    wordsToBytes: function(t) {
        for (var e = [], n = 0; n < 32 * t.length; n += 8) e.push(t[n >>> 5] >>> 24 - n % 32 & 255);
        return e
    },
    bytesToHex: function(t) {
        for (var e = [], n = 0; n < t.length; n++) e.push((t[n] >>> 4).toString(16)), e.push((15 & t[n]).toString(16));
        return e.join("")
    },
    hexToBytes: function(t) {
        for (var e = [], n = 0; n < t.length; n += 2) e.push(parseInt(t.substr(n, 2), 16));
        return e
    },
    bytesToBase64: function(t) {
        for (var n = [], i = 0; i < t.length; i += 3)
            for (var o = t[i] << 16 | t[i + 1] << 8 | t[i + 2], r = 0; r < 4; r++) 8 * i + 6 * r <= 8 * t.length ? n.push(e.charAt(o >>> 6 * (3 - r) & 63)) : n.push("=");
        return n.join("")
    },
    base64ToBytes: function(t) {
        t = t.replace(/[^A-Z0-9+\/]/gi, "");
        for (var n = [], i = 0, o = 0; i < t.length; o = ++i % 4) 0 != o && n.push((e.indexOf(t.charAt(i - 1)) & Math.pow(2, -2 * o + 8) - 1) << 2 * o | e.indexOf(t.charAt(i)) >>> 6 - 2 * o);
        return n
    },
    utf8: {
        stringToBytes: function(t) {
            return n.bin.stringToBytes(unescape(encodeURIComponent(t)))
        },
        bytesToString: function(t) {
            return decodeURIComponent(escape(n.bin.bytesToString(t)))
        }
    },
    bin: {
        stringToBytes: function(t) {
            for (var e = [], n = 0; n < t.length; n++)
                e.push(255 & t.charCodeAt(n));
            return e
        },
        bytesToString: function(t) {
            for (var e = [], n = 0; n < t.length; n++)
                e.push(String.fromCharCode(t[n]));
            return e.join("")
        }
    }
},
e=n,
r = n.bin,
i = n.utf8,
s = function(t, n) {
    t.constructor == String ? t = n && "binary" === n.encoding ? r.stringToBytes(t) : i.stringToBytes(t) : o(t) ? t = Array.prototype.slice.call(t, 0) : Array.isArray(t) || (t = t.toString());
    for (var a = e.bytesToWords(t), l = 8 * t.length, c = 1732584193, u = -271733879, h = -1732584194, f = 271733878, p = 0; p < a.length; p++)
        a[p] = 16711935 & (a[p] << 8 | a[p] >>> 24) | 4278255360 & (a[p] << 24 | a[p] >>> 8);
    a[l >>> 5] |= 128 << l % 32,
    a[14 + (l + 64 >>> 9 << 4)] = l;
    var d = ff
      , b = gg
      , T = hh
      , g = ii;
    for (p = 0; p < a.length; p += 16) {
        var v = c
          , S = u
          , m = h
          , A = f;
        u = g(u = g(u = g(u = g(u = T(u = T(u = T(u = T(u = b(u = b(u = b(u = b(u = d(u = d(u = d(u = d(u, h = d(h, f = d(f, c = d(c, u, h, f, a[p + 0], 7, -680876936), u, h, a[p + 1], 12, -389564586), c, u, a[p + 2], 17, 606105819), f, c, a[p + 3], 22, -1044525330), h = d(h, f = d(f, c = d(c, u, h, f, a[p + 4], 7, -176418897), u, h, a[p + 5], 12, 1200080426), c, u, a[p + 6], 17, -1473231341), f, c, a[p + 7], 22, -45705983), h = d(h, f = d(f, c = d(c, u, h, f, a[p + 8], 7, 1770035416), u, h, a[p + 9], 12, -1958414417), c, u, a[p + 10], 17, -42063), f, c, a[p + 11], 22, -1990404162), h = d(h, f = d(f, c = d(c, u, h, f, a[p + 12], 7, 1804603682), u, h, a[p + 13], 12, -40341101), c, u, a[p + 14], 17, -1502002290), f, c, a[p + 15], 22, 1236535329), h = b(h, f = b(f, c = b(c, u, h, f, a[p + 1], 5, -165796510), u, h, a[p + 6], 9, -1069501632), c, u, a[p + 11], 14, 643717713), f, c, a[p + 0], 20, -373897302), h = b(h, f = b(f, c = b(c, u, h, f, a[p + 5], 5, -701558691), u, h, a[p + 10], 9, 38016083), c, u, a[p + 15], 14, -660478335), f, c, a[p + 4], 20, -405537848), h = b(h, f = b(f, c = b(c, u, h, f, a[p + 9], 5, 568446438), u, h, a[p + 14], 9, -1019803690), c, u, a[p + 3], 14, -187363961), f, c, a[p + 8], 20, 1163531501), h = b(h, f = b(f, c = b(c, u, h, f, a[p + 13], 5, -1444681467), u, h, a[p + 2], 9, -51403784), c, u, a[p + 7], 14, 1735328473), f, c, a[p + 12], 20, -1926607734), h = T(h, f = T(f, c = T(c, u, h, f, a[p + 5], 4, -378558), u, h, a[p + 8], 11, -2022574463), c, u, a[p + 11], 16, 1839030562), f, c, a[p + 14], 23, -35309556), h = T(h, f = T(f, c = T(c, u, h, f, a[p + 1], 4, -1530992060), u, h, a[p + 4], 11, 1272893353), c, u, a[p + 7], 16, -155497632), f, c, a[p + 10], 23, -1094730640), h = T(h, f = T(f, c = T(c, u, h, f, a[p + 13], 4, 681279174), u, h, a[p + 0], 11, -358537222), c, u, a[p + 3], 16, -722521979), f, c, a[p + 6], 23, 76029189), h = T(h, f = T(f, c = T(c, u, h, f, a[p + 9], 4, -640364487), u, h, a[p + 12], 11, -421815835), c, u, a[p + 15], 16, 530742520), f, c, a[p + 2], 23, -995338651), h = g(h, f = g(f, c = g(c, u, h, f, a[p + 0], 6, -198630844), u, h, a[p + 7], 10, 1126891415), c, u, a[p + 14], 15, -1416354905), f, c, a[p + 5], 21, -57434055), h = g(h, f = g(f, c = g(c, u, h, f, a[p + 12], 6, 1700485571), u, h, a[p + 3], 10, -1894986606), c, u, a[p + 10], 15, -1051523), f, c, a[p + 1], 21, -2054922799), h = g(h, f = g(f, c = g(c, u, h, f, a[p + 8], 6, 1873313359), u, h, a[p + 15], 10, -30611744), c, u, a[p + 6], 15, -1560198380), f, c, a[p + 13], 21, 1309151649), h = g(h, f = g(f, c = g(c, u, h, f, a[p + 4], 6, -145523070), u, h, a[p + 11], 10, -1120210379), c, u, a[p + 2], 15, 718787259), f, c, a[p + 9], 21, -343485551),
        c = c + v >>> 0,
        u = u + S >>> 0,
        h = h + m >>> 0,
        f = f + A >>> 0
    }
    return e.endian([c, u, h, f])
},

ff = function(t, e, n, i, o, r, s) {
    var a = t + (e & n | ~e & i) + (o >>> 0) + s;
    return (a << r | a >>> 32 - r) + e
}, gg = function(t, e, n, i, o, r, s) {
    var a = t + (e & i | n & ~i) + (o >>> 0) + s;
    return (a << r | a >>> 32 - r) + e
}, hh = function(t, e, n, i, o, r, s) {
    var a = t + (e ^ n ^ i) + (o >>> 0) + s;
    return (a << r | a >>> 32 - r) + e
}, ii = function(t, e, n, i, o, r, s) {
    var a = t + (n ^ (e | ~i)) + (o >>> 0) + s;
    return (a << r | a >>> 32 - r) + e
}, 

gen_appsign = function(t, n) {
    if (void 0 === t || null === t)
        throw new Error("Illegal argument " + t);
    var i = e.wordsToBytes(s(t, n));
    return n && n.asBytes ? i : n && n.asString ? r.bytesToString(i) : e.bytesToHex(i)
};



//exports.gen_sign = gen_sign