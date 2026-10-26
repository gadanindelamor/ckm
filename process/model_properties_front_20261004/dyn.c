/* Port 1:1 del loop de dinámica de scripts/optimalmodularity.jl (beliefnet, Aiyappa et al.).
   Todo lo aleatorio viene pregenerado desde Python (numpy), en el mismo orden de consumo que el Julia:
   arista, dirección, belief focal, ruido gaussiano. */
void dinamica(int T, const int *esrc, const int *edst, const int *eidx, const int *dir,
              const int *focal, const double *gauss, double *B /* N x 3 */, const int *fijo,
              double alpha, double beta, double sigma) {
    for (int t = 0; t < T; t++) {
        int e = eidx[t];
        int sender, receiver;
        if (dir[t] == 0) { sender = esrc[e]; receiver = edst[e]; }
        else             { sender = edst[e]; receiver = esrc[e]; }
        if (fijo[receiver]) continue;
        int f = focal[t];
        double bs = B[3*sender + f], br = B[3*receiver + f];
        double der = 1.0;                       /* -1 * dE/db = producto de las otras dos */
        for (int k = 0; k < 3; k++) if (k != f) der *= B[3*receiver + k];
        double mu = alpha*bs + beta*der;
        double nb = br + (mu + sigma*gauss[t]);
        if (nb > 1) nb = 1; else if (nb < -1) nb = -1;
        B[3*receiver + f] = nb;
    }
}
