#!/usr/bin/env python3
import sys
import datetime
import matplotlib.pyplot as plt
import argparse


class CapInt:
  
  def __init__(self) :
    self.cap_semplice = lambda C, i, t : C + C*i*t
    self.cap_composta = lambda C, i, t : C * (1+i)**t
    self.periodo = { 'semestrale':2, 'trimestrale':4, 'quadrimestrale':3, 'annuale':1 }
    self.cap_ = self.cap_composta
    self.periodo_ = self.periodo['annuale']
    self.print_allreport = False

  def set_cap_semplice(self) :
    self.cap_ = self.cap_semplice

  def set_periodo(self, sem) :
    self.periodo_ = self.periodo[sem]

  def do_saldo(self, C, i, t) :
    assert(isinstance(C, float) and isinstance(i, float) and isinstance(t, float))
    self.saldo = self.cap_(C, i, t*self.periodo_)
    return self.saldo


  def do_graph(self, C, i, t) :
    timenow = datetime.datetime.now()
    year = timenow.year
    saldo = C
    interesse = i
    durata = t
    self.anno_interesse = { year : (saldo,interesse) }

    for x in range(durata) :
      saldo = cp.do_saldo(saldo, interesse, 1.)
      self.anno_interesse.update({year+x+1:(saldo,interesse)})

    orderz = self.do_print()
    self.print_stat(orderz)


  def do_print(self):
    orderz = [(year, (bill,perc)) for year,(bill,perc) in sorted(self.anno_interesse.items(), key=lambda x: x[0])]
    orderz_tmp = orderz
    if not self.print_allreport :
      orderz_tmp = [ orderz[0], orderz[int(len(orderz)/2)], orderz[-1] ]
    for year,(bill,perc) in orderz_tmp:
      print("[{0}] - {1}; {2};".format(year, int(bill), perc))
    return orderz


  def print_stat(self, orderz):
    first_year = orderz[0][0]
    last_year = orderz[-1][0]
    bills = []
    years = []

    for year_now, bill_now in [(year,bill[0]) for year,bill in orderz]:
      years.append(int(year_now))
      bills.append(bill_now)

    plt.plot(years, bills)
    plt.xlabel('Anno')
    plt.ylabel('Saldo')
    plt.title("Year {0} - {1}".format(first_year, last_year))
    plt.grid(True)
    plt.savefig("output_{0}_{1}".format(first_year, last_year))
    plt.close()


if __name__ == "__main__":

  cp = CapInt()
  parser = argparse.ArgumentParser()

  parser.add_argument( '-capitale' ,\
                       type=float,\
                       required=True,\
                       help="Capitale inizialmente depositato")

  parser.add_argument( '-interesse',\
                       type=float,\
                       required=True,\
                       help="Interesse da maturare")

  parser.add_argument( '-durata',\
                       type=int,\
                       required=True,\
                       help="Durata deposito in anni")

  parser.add_argument( '-cap_semplice' ,\
                       action="store_true" ,\
                       default=False ,\
                       help="Usa formula della capitalizzazione semplice, di default viene usata quella composta")

  parser.add_argument( '-periodo',\
                       choices=["annuale", "semestrale","trimestrale","quadrimestrale"],\
                       default="annuale",\
                       help="Unità di riferimento del tasso d'interesse")

  parser.add_argument( '-print_allreport' ,\
                       action="store_true" ,\
                       default=False ,\
                       help="Stampa da linea di comando ogni anno saldo e relativo interesse, invece di 1-quartile, mediana, 4-quartile della distribuzione")


  args = parser.parse_args()

  cp = CapInt()
  cp.set_periodo(args.periodo)
  if args.cap_semplice :
    cp.set_cap_semplice()
  if args.print_allreport :
    cp.print_allreport = True

  cp.do_graph(args.capitale, args.interesse, args.durata)


