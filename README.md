# Fair Exchange

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

<h1>Molina's Architecture:</h1>

<img src="/images/architecture(Molina).jpg" alt="Molina's Architecture">

<ol>
<li> Applications send their items DA and DB to be encrypted;</li>
<li> The attestables deposit [DA] and [DB];</li>
<li> The attestables verify the items and generate tokens to be sent to the PBB;</li>
<li> The tokens are posted on the PBB;</li>
<li> The tokens are retrieved from the PBB;</li>
<li> The items are released (Alice will have DB and Bob will have DA).</li>
</ol>


<h1>Propriedades da Arquitetura do Molina</h1>

<ul>
<li> </li>
<li> </li>
<li> </li>
<li> </li>
<li> </li>
<li> </li>
</ul>

<h1>KiT's Architecture:</h1>

<img src="/images/architecture(KiT).jpg" alt="KiT's Architecture">

<h3>Fair Exchange Program</h3>

<ol>
<li> Receive kA from PA;</li>
<li> Establish a secure channel with GB through PA;</li>
<li> Send kA to GB through the channel;</li>
<li> Receive kB from GB through the channel;</li>
<li> Check kB, if incorrect, abort;</li>
<li> Encrypt kB with a random secret key K;</li>
<li> Send kB encrypted with K to PA;</li>
<li> Execute the Synchronization Protocol;</li>
<li> if the synchronization failed then abort;</li>
<li> Send K to PA.</li>
</ol>

<h1>KiT's Synchronization:</h1>

<img src="/images/Synchronization(KiT).jpg" alt="KiT's Synchronization">


<h3>Synchronization Program</h3>

<ol>
<li> Send a random value C to GB;</li>
<li>   while C>0 do</li>
    <ul>
      <li> Standby {waitfor a message or a timeout};</li>
      <li>  if a timeoutfrom PA is received then the synchronization failed;</li>
      <li> {a message from GB is received} decrement C;</li>
      <li> if C =0 then the synchronization succeeded;</li>
      <li> Send an message to GB and decrement C;</li>
    </ul>
<li> end while</li>
<li> Standby {wait for a timeout};</li>
<li> The synchronization succeeded.</li>
</ol>


<h1>Arquitetura :</h1>
