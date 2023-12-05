#include "rs-simulation.h"

#include <iostream>
#include <cstdint>
#include <itpp/itcomm.h>

using namespace itpp;

///////////////////////////////////////////////////////////////////////////////
// Código copiado para evitar "quebra" do IT++
GFX formal_derivate(const GFX &f)
{
  int degree = f.get_true_degree();
  int q = f.get_size();
  int i;
  GFX fprim(q, degree);
  fprim.clear();
  for (i = 0; i <= degree - 1; i += 2) {
    fprim[i] = f[i + 1];
  }
  return fprim;
}

bool Reed_Solomon::decode(const bvec &coded_bits, const ivec &erasure_positions, bvec &decoded_message, bvec &cw_isvalid)
{
  bool decoderfailure, no_dec_failure;
  int j, i, kk, l, L, foundzeros, iterations = floor_i(static_cast<double>(coded_bits.length()) / (n * m));
  bvec mbit(m * k);
  decoded_message.set_size(iterations * k * m, false);
  cw_isvalid.set_length(iterations);

  GFX rx(q, n - 1), cx(q, n - 1), mx(q, k - 1), ex(q, n - 1), S(q, 2 * t), Xi(q, 2 * t), Gamma(q), Lambda(q),
      Psiprime(q), OldLambda(q), T(q), Omega(q);
  GFX dummy(q), One(q, (char*)"0"), Omegatemp(q);
  GF delta(q), tempsum(q), rtemp(q), temp(q), Xk(q), Xkinv(q);
  ivec errorpos;

  if ( erasure_positions.length() ) {
    it_assert(max(erasure_positions) < iterations*n, "Reed_Solomon::decode: erasure position is invalid.");
  }
  
  no_dec_failure = true;
  for (i = 0; i < iterations; i++) {
    decoderfailure = false;
    //Fix the received polynomial r(x)
    for (j = 0; j < n; j++) {
      rtemp.set(q, coded_bits.mid(i * n * m + j * m, m));
      rx[j] = rtemp;
    }
    // Fix the Erasure polynomial Gamma(x)
    // and replace erased coordinates with zeros
    rtemp.set(q, -1);
    ivec alphapow = - ones_i(2);
    Gamma = One;
    for (j = 0; j < erasure_positions.length(); j++) {
      rx[erasure_positions(j)] = rtemp;
      alphapow(1) = erasure_positions(j);
      Gamma *= (One - GFX(q, alphapow));
    }
    //Fix the syndrome polynomial S(x).
    S.clear();
    for (j = 1; j <= 2 * t; j++) {
      S[j] = rx(GF(q, b + j - 1));
    }
    // calculate the modified syndrome polynomial Xi(x) = Gamma * (1+S) - 1
    Xi = Gamma * (One + S) - One;
    // Apply Berlekam-Massey algorithm
    if (Xi.get_true_degree() >= 1) { //Errors in the received word
      // Iterate to find Lambda(x), which hold all error locations
      kk = 0;
      Lambda = One;
      L = 0;
      T = GFX(q, (char*)"-1 0");
      while (kk < 2 * t) {
        kk = kk + 1;
        tempsum = GF(q, -1);
        for (l = 1; l <= L; l++) {
          tempsum += Lambda[l] * Xi[kk - l];
        }
        delta = Xi[kk] - tempsum;
        if (delta != GF(q, -1)) {
          OldLambda = Lambda;
          Lambda -= delta * T;
          if (2 * L < kk) {
            L = kk - L;
            T = OldLambda / delta;
          }
        }
        T = GFX(q, (char*)"-1 0") * T;
      }
      // Find the zeros to Lambda(x)
      errorpos.set_size(Lambda.get_true_degree());
      foundzeros = 0;
      for (j = q - 2; j >= 0; j--) {
        if (Lambda(GF(q, j)) == GF(q, -1)) {
          errorpos(foundzeros) = (n - j) % n;
          foundzeros += 1;
          if (foundzeros >= Lambda.get_true_degree()) {
            break;
          }
        }
      }
      if (foundzeros != Lambda.get_true_degree()) {
        decoderfailure = true;
      }
      else { // Forney algorithm...
        //Compute Omega(x) using the key equation for RS-decoding
        Omega.set_degree(2 * t);
        Omegatemp = Lambda * (One + Xi);
        for (j = 0; j <= 2 * t; j++) {
          Omega[j] = Omegatemp[j];
        }
        //Find the error/erasure magnitude polynomial by treating them the same
        Psiprime = formal_derivate(Lambda*Gamma);
        errorpos = concat(errorpos, erasure_positions);
        ex.clear();
        for (j = 0; j < errorpos.length(); j++) {
          Xk = GF(q, errorpos(j));
          Xkinv = GF(q, 0) / Xk;
          // we calculate ex = - error polynomial, in order to avoid the 
          // subtraction when recunstructing the corrected codeword
          ex[errorpos(j)] = (Xk * Omega(Xkinv)) / Psiprime(Xkinv);
          if (b != 1) { // non-narrow-sense code needs corrected error magnitudes
            int correction_exp = ( errorpos(j)*(1-b) ) % n;
            ex[errorpos(j)] *= GF(q, correction_exp + ( (correction_exp < 0) ? n : 0 ));
          }
        }
        //Reconstruct the corrected codeword.
        // instead of subtracting the error/erasures, we calculated 
        // the negative error with 'ex' above
        cx = rx + ex;
        //Code word validation
        S.clear();
        for (j = 1; j <= 2 * t; j++) {
          S[j] = cx(GF(q, b + j - 1));
        }
        if (S.get_true_degree() >= 1) {
          decoderfailure = true;
        }
      }
    }
    else {
      cx = rx;
      decoderfailure = false;
    }
    //Find the message polynomial
    mbit.clear();
    if (decoderfailure == false) {
      if (cx.get_true_degree() >= 1) { // A nonzero codeword was transmitted
        if (systematic) {
          for (j = 0; j < k; j++) {
            mx[j] = cx[j];
          }
        }
        else {
          mx = divgfx(cx, g);
        }
        for (j = 0; j <= mx.get_true_degree(); j++) {
          mbit.replace_mid(j * m, mx[j].get_vectorspace());
        }
      }
    }
    else { //Decoder failure.
      // for a systematic code it is better to extract the undecoded message
      // from the received code word, i.e. obtaining a bit error
      // prob. p_b << 1/2, than setting all-zero (p_b = 1/2)
      if (systematic) {
        mbit = coded_bits.mid(i * n * m, k * m);
      }
      else {
        mbit = zeros_b(m*k);
      }
      no_dec_failure = false;
    }
    decoded_message.replace_mid(i * m * k, mbit);
    cw_isvalid(i) = (!decoderfailure);
  }
  return no_dec_failure;
}

///////////////////////////////////////////////////////////////////////////////

RsSimulation::RsSimulation(int32_t nbits, int32_t MaxIterations, int32_t MaxErrors) :
    Nbits(nbits), MaxIterations(MaxIterations), MaxErrors(MaxErrors)
{
    RNG_randomize();
}

RsSimulation::~RsSimulation()
{

}

int32_t RsSimulation::Run()
{
    vec EbN0dB = linspace(0, 4, 16);
    vec EbN0 = inv_dB(EbN0dB);

    AWGN_Channel awgn_Channel;
    BPSK bpsk;
    BERC berc;
    Reed_Solomon rs(8, 16);

    vec ber;
    ber.set_size(EbN0dB.length(), false);
    ber.clear();

    // Determinar Eb a partir de Ec
    double Ec = 1.0;
    double Eb = Ec / rs.get_rate();

    // Calculando os valores de N0 para todos os EbN0
    vec N0 = Eb*pow(EbN0, -1);

    for (int32_t p = 0; p < EbN0dB.length(); p++) {
        std::cout << "Simulando ponto " << p + 1 << " de " << EbN0dB.length() << std::endl;

        berc.clear();
        awgn_Channel.set_noise(N0(p) / 2.0);

        for (int32_t i = 0; i < this->MaxIterations; i++) {
            bvec rec_bits, bits = randb(this->Nbits);
            // Encode RS(255, 223)
            bvec coded_bits = rs.encode(bits);
            vec trans_symbols;
            // Modular BPSK
            bpsk.modulate_bits(coded_bits, trans_symbols);
            // Passar no canal AWGN
            vec rec_symbols = awgn_Channel(trans_symbols);
            // Demodular BPSK
            bpsk.demodulate_bits(rec_symbols, rec_bits);
            // Decode RS(255, 223)
            bvec decoded_bits;
            bvec cw_isvalid;
            if (rs.decode(rec_bits, decoded_bits, cw_isvalid) == false) {
                std::cout << "Oopsie poosie..." << std::endl;
                return E_DECODING_FAILED;
            }
            berc.count(bits, rec_bits);
            ber(p) = berc.get_errorrate();
            if (berc.get_errors() > this->MaxErrors) {
                std::cout << "Saindo do ponto " << p + 1 << " com " << berc.get_errors() << " erros." << std::endl;
                break;
            }
        }
    }

    std::cout << "Resultado final: " << std::endl;
    std::cout << "ber, ebn0db" << std::endl;
    for (int32_t i = 0; i < ber.length(); i++) {
        std::cout << ber(i) << ", " << EbN0dB(i) << std::endl;
    }

    return SimulationSuccess::E_SUCCESS;
}