/* ============================================================
   match.js — recommendation scoring
   Combines: desired<->offered cross-match, mutual swap bonus,
   skill-level compatibility, and the candidate's rating.
   ============================================================ */
const LEVELS = { Beginner: 1, Intermediate: 2, Advanced: 3 };

function computeMatch(me, cand){
  const lines = [];
  let score = 0;

  if(!me.offered.length || !me.desired.length){
    return { score: 0, lines: [{ ok:false, text:"Complete your profile to see a match score." }], mutual:false };
  }

  const meWants = me.desired[0];
  const meOffers = me.offered[0];
  const theyOffer = cand.offered[0];
  const theyWant = cand.desired[0];

  const theyOfferWhatIWant =
    theyOffer.skill.toLowerCase().includes(meWants.skill.toLowerCase()) ||
    meWants.skill.toLowerCase().includes(theyOffer.skill.split(" ")[0].toLowerCase());

  const theyWantWhatIOffer =
    theyWant.skill.toLowerCase().includes(meOffers.skill.toLowerCase()) ||
    meOffers.skill.toLowerCase().includes(theyWant.skill.split(" ")[0].toLowerCase());

  if(theyOfferWhatIWant){
    score += 35;
    lines.push({ ok:true, text:`They offer ${theyOffer.skill} (${theyOffer.level}) ↔ you want ${meWants.skill} (${meWants.level})` });
  } else {
    lines.push({ ok:false, text:`They offer ${theyOffer.skill} — not on your want list` });
  }

  if(theyWantWhatIOffer){
    score += 35;
    lines.push({ ok:true, text:`They want ${theyWant.skill} (${theyWant.level}) ↔ you offer ${meOffers.skill} (${meOffers.level})` });
  } else {
    lines.push({ ok:false, text:`They want ${theyWant.skill} — not on your offer list` });
  }

  if(theyOfferWhatIWant){
    const diff = LEVELS[theyOffer.level] - LEVELS[meWants.level];
    score += diff >= 0 ? 15 : 6;
  }

  score += Math.round((cand.rating / 5) * 15);

  return { score: Math.min(score, 99), lines, mutual: theyOfferWhatIWant && theyWantWhatIOffer };
}
