<template>
  <base-app>
    <v-container
        id="typography"
        fluid
        tag="section"
      >
        <v-row
          align="center"
          justify="center"
        >
          <v-col cols="12">
            <base-material-card
              icon="mdi-alphabetical"
            >
              <v-card-text>
                <v-container
                  class="pa-0"
                  fluid
                >
                  <v-row
                    v-for="(t, i) in typography"
                    :key="i"
                    align="center"
                  >
                    <v-col
                      cols="1"
                      md="3"
                    >
                      <span
                        class="tim-note"
                        v-text="t[0]"
                      />
                    </v-col>
                    <v-col cols="8">
                      <p>
                        {{ t[1] }}
                      </p>
                    </v-col>
                  </v-row>
                </v-container>
              </v-card-text>
            </base-material-card>
          </v-col>
        </v-row>
      </v-container>
  </base-app>
</template>

<script>
  import VFormBase from 'vuetify-form-base'

  export default {
    name: 'index',
    components: {
      VFormBase
    },
    data () {
      return {
        typography: [
          ['a. dir.', 'Anv direizh'],
          ['a. ls.', 'Anv lies'],
          ['AAA', 'aaa'],
          ['adls.', 'Adliester'],
          ['adv.', 'Adverb'],
          ['ag.', 'Anv-gwan'],
          ['agv.', 'Anv-gwan verb'],
          ['ak.', 'Anv-kadarn'],
          ['am.', 'Amresis'],
          ['amr.', 'Amreizh'],
          ['ar.', 'Araogenn'],
          ['ar. kim.', 'Arouez kimiek'],
          ['av.', 'Anv-verb'],
          ['B.', 'Anv benel'],
          ['b./g.', 'Benel peurliesañ, gourel a-wechoù'],
          ['BARZH.', 'Barzhoniezh'],
          ['BEVON.', 'Bevoniezh'],
          ['blot.', 'Blotaat'],
          ['bnk.', 'Bennak'],
          ['BUGALE', 'Termen, teneraus peurliesañ, a reer gantañ evit komz ouzh ar vugale vihan'],
          ['c\'hwezh.', 'C\'hwezañ'],
          ['d.', 'Anv daou'],
          ['d.l.e.', 'Da lavaret eo'],
          ['da sk.', 'Da skouer'],
          ['damskoaz.', 'Damskoazell'],
          ['darn.', 'Darnel'],
          ['db.', 'Diwar-benn'],
          ['dg.', 'Dibenn-ger'],
          ['dh.', 'Dreist-holl'],
          ['DHS', 'Ger(ioù) damheñvelster'],
          ['dibers.', 'Dibersonel'],
          ['diren.', 'Direnadenn'],
          ['dish. diouzh', 'Disheñvel diouzh'],
          ['disk.', 'Diskouez'],
          ['dismeg.', 'Dismegañsus'],
          ['displ.', 'Displeget'],
          ['DISPRED.', 'Termen dispredet, aet er-maez implij'],
          ['divin.', 'Divinadell'],
          ['diw. c\'hoap', 'Diwar c\'hoap'],
          ['diw. vousgoap', 'Diwar vousgoap'],
          ['DIZIMPL.', 'Termen aet er-maez implij'],
          ['doar.', 'Doareenn'],
/*
doar./stn.
Doareenn ha stagenn
doare diskl.
Doare-disklêriañ
doare div.
Doare-divizout
doare gourc'h.
Doare-gourc'hemenn
DOUAR.
Termen douaroniel
DOUAROUR.
Douarouriezh
dre ast.
Dre astenn-ster
dre c'hwez.
Dre c'hwezañ
dre eilp.
Dre eilpenn-ster
dre gunuj.
Dre gunujañ
dre heveleb.
Dre hevelebiezh
dre ledanv.
Dre ledanviñ
dre let.
Dre leterc'hañ
dre seven.
Dre sevended
dre skeud.
Dre skeudenn-lavar
dre verr.
Dre verrdro
dre zeread.
Dre zereadegezh
dre zic'harv.
Dre zic'harvaat
Dre zismeg.
Dre zismegañs
e.
Eeun
em.
Emober
erlerc'h.
Erlerc'hiañ
ES
Enepster
estl.
Estlammadell
EVEZH.
Evezhiadenn
EVNON.
Evnoniezh
f.
Furm
fent.
Fentus
G.
Anv gourel
g. niv.
Ger niveriñ
g. perc'h.
Ger perc'hennañ
g. pouez.
Ger pouezañ
g. pouez. didon
Ger pouezañ didon
g. pouez. toniet
Ger pouezañ toniet
g./b.
Gourel peurliesañ, benel a-wechoù
GALLEK.
Gallekadur, amprest diezhomm digant ar galleg
gelv.
Gelver
gm.
Ger-mell
gm. a.
Ger-mell amstrizh
gm. s.
Ger-mell strizh
goap.
Goapaus
goul.
Goulenn
GOUNEZ.
Gounezerezh
GREANT.
Greanterezh
GWENGEL.
Gwengelouriezh
h.
Anv hollek
h.a.
Hag all
h.b.
Anv hollek benel
h.b./h.g.
Anv hollek benel peurliesañ, gourel a-wechoù
h.g.
Anv hollek gourel
h.g./h.b.
Anv hollek gourel peurliesañ, benel a-wechoù
HENON.
Henoniezh
het.
Hetiñ
HINOUR.
Hinouriezh
HS
Ger(ioù) heñvelster
impl. da
Implijet da
islav.
Islavarenn
isur.
Isurzhiañ
JEDON.
Jedoniezh
k.
Kreñv
k.d.
Kreñv dieeun
k.e.
Kreñv eeun
kad.
Kadarnaat
kal.
Kaletaat
KAN.
Kanaouenn
KEGIN.
Keginerezh
KELENN.
Kelennerezh
KEMBRAEK.
Kembraekadur, amprest diezhomm digant ar c'hembraeg.
kemm.
Kemmadur
kenem.
Kenemober
kenur.
Kenurzhiañ
KEVREDAD.
Kevredadouriezh
KORF.
Korfadurezh
krl.
Krennlavar
kunuj.
Kunujennus
kv.
Keñveriañ
lav.
Lavarenn
LENN.
Lennegezh
lg.
Lostger
LIORZH.
Liorzherezh
LIVOUR.
Livouriezh
LOENON.
Loenoniezh
LOUZAWOUR.
Louzawouriezh
ls.
Liester
luc'h.
Luc'haj
MELESTR.
Melestradurezh
MENTON.
Mentoniezh
MERDEAD
Merdeadurezh
mesk.
Mesket
MEZEG.
Mezegiezh
MOULL.
Moullerezh
niver.
Niver
NIVERON.
Niveroniezh
p.
Pajenn
peg.
Pegementiñ
PEMDEZ
Termen a reer gantañ er yezh pemdez, laoskoc'h, enebet ouzh un termen all, furmeloc'h
pennlav.
Pennlavarenn
perc'h.
Perc'hennañ
pet.
Petvediñ
pg
Pennger
POLITIK.
Politikerezh
pouez.
Pouezañ
PREDER.
Prederouriezh
prl.
Peurliesañ
rag.
Raganv
rannyezh.
Termen rannyezhel
RELIJ.
Relijion
rn.
Rannig
s.o.
Sellout ouzh
SAOZNEK.
Saoznekadur, amprest diezhomm digant ar saozneg
SAVOUR.
Savouriezh
sk.
Skoazell
skeud.
Skeudennek
SKIANT. NAT.
Skiantoù naturel
st.
Stumm
STEREDON.
Steredoniezh
STEREDOUR.
Steredouriezh
stl.
Stagell
STLENN.
Stlenneg
stn.
Stagenn
str.
Stroll
SURJIAN.
Surjianerezh
tr.
Troienn
TRELOC'H.
Treloc'herezh
trl.
Tro-lavar
u.
Unanderenn
ub.
Unan bennak
udb.
Un dra bennak
v.
Verb
vkd.
Verb kreñv dieeun
vke.
Verb kreñv eeun
YEZHAD.
Yezhadur
YEZHON.
Yezhoniezh*/
        ]
      }
    },
  }
</script>

<style lang="scss">
  .tim-note {
    bottom: 10px;
    // color: #c0c1c2;
    display: block;
    font-weight: 400;
    font-size: 15px;
    line-height: 13px;
    left: 0;
    margin-left: 20px;
    width: 260px;
  }
</style>
