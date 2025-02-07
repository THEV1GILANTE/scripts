/**
 * Experimental Miner Demo – Connects to a Kryptex pool endpoint.
 * 
 * Usage:
 *   node miner.js [--ssl]
 *
 * Without --ssl, it uses TCP to connect to sal.kryptex.network:7777.
 * With --ssl, it uses TLS to connect to sal-eu.kryptex.network:7028.
 *
 * NOTE: This demo only connects and sends a simple mining.subscribe message.
 * A real miner must implement job parsing, hashing loops, share submission, etc.
 */

const net = require('net');
const tls = require('tls');

// Determine whether to use SSL based on command-line argument.
const useSSL = process.argv.includes('--ssl');

const poolHost = useSSL ? 'sal-eu.kryptex.network' : 'sal.kryptex.network';
const poolPort = useSSL ? 7028 : 7777;

console.log(`Starting experimental miner:
  Connection type: ${useSSL ? 'SSL/TLS' : 'TCP'}
  Pool: ${poolHost}:${poolPort}
  Region: Europe (if using SSL) / Global (if using TCP)
`);

function onConnect() {
  console.log(`Connected to ${poolHost}:${poolPort} using ${useSSL ? 'SSL/TLS' : 'TCP'}`);
  
  // Prepare a basic mining.subscribe message as per Stratum protocol
  const subscribeMsg = JSON.stringify({
    id: 1,
    method: 'mining.subscribe',
    params: [] // In a real miner, parameters might be required.
  }) + "\n";

  console.log("Sending subscription request:", subscribeMsg.trim());
  client.write(subscribeMsg);
}

const client = useSSL ?
  tls.connect(poolPort, poolHost, {}, onConnect) :
  net.connect(poolPort, poolHost, onConnect);

client.setEncoding('utf8');

client.on('data', (data) => {
  console.log("Received from pool:", data.trim());
  // In a full miner, you would parse the JSON-RPC messages here,
  // look for 'mining.notify' calls, and start a hash-computation loop.
});

client.on('error', (err) => {
  console.error("Connection error:", err);
});

client.on('end', () => {
  console.log("Disconnected from pool.");
});
