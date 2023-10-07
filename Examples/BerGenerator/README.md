# BER Generator

Código de exemplo para geração de BER usando o GNU Radio. Esse exemplo funciona no GNU Radio 3.10, que tem alguns problemas na utilização do "BER Curve Gen". e "QT GUI Bercurve Sink". Isso é possível graças a um post no GitHub que explica como fazer pra funcionar:

https://github.com/gnuradio/gnuradio/issues/5627#issuecomment-1060608139

Com essa explicação agora foi possível gerar a curva BER no GNU Radio usando o "Dummy Encoder" e "Dummy Decoder".
