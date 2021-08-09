#!/usr/bin/perl

#Read the file with rankings
open RANKING,"<", $ARGV[0];
#Load it to an array
my @ranking = <RANKING>;
#Arrays to hold values for each ranking
my @ssim = ();
my @psnr = ();
my @mse = ();
my @nmse = ();
my @visual = ();

#Temporary array to hold each line of iteration
my @temp = ();

#Loop to load the rankings from the ranking array containing each line of the file, 
#to respective ranking arrays
foreach (@ranking) {
    @temp = split(" ",$_);
    #print($temp[3]."\n");
    push @visual,$temp[0];
    push @ssim,$temp[1];
    push @psnr,$temp[3];
    push @mse,$temp[2];
    push @nmse,$temp[4];
}

#removing unwanted things from the end of the arrrays.
pop(@visual);
pop(@visual);
pop(@ssim);
pop(@ssim);
pop(@psnr);
pop(@psnr);
pop(@mse);
pop(@mse);
pop(@nmse);
pop(@nmse);

#Calculate SSIM Ranking's score w.r.t. Visual Ranking
my $i = 0;
my $index = 0;
my $ssim_score = 0;
foreach my $value (@ssim){
    for (my $j = 0; $j <= $#visual; $j= $j+1){
        if($visual[$j] eq $value){
            $index = $j;
        }
    }
    if (abs($index - $i) < 5){
        $ssim_score = $ssim_score + 1;
    } elsif (abs($index - $i) > 7){
        $ssim_score = $ssim_score - 2;
    } elsif (abs($index - $i) > 4){
        $ssim_score = $ssim_score - 1;
    }
    $i++;
}

#Calculate PSNR Ranking's score w.r.t. Visual Ranking
$i = 0;
$index = 0;
my $psnr_score = 0;
foreach my $value (@psnr){
    for (my $j = 0; $j <= $#visual; $j= $j+1){
        if($visual[$j] eq $value){
            $index = $j;
        }
    }
    if (abs($index - $i) < 5){
        $psnr_score = $psnr_score + 1;
    } elsif (abs($index - $i) > 7){
        $psnr_score = $psnr_score - 2;
    } elsif (abs($index - $i) > 4){
        $psnr_score = $psnr_score - 1;
    }
    $i++;
}

#Calculate MSE Ranking's score w.r.t. Visual Ranking
$i = 0;
$index = 0;
my $mse_score = 0;
foreach my $value (@mse){
    for (my $j = 0; $j <= $#visual; $j= $j+1){
        if($visual[$j] eq $value){
            $index = $j;
        }
    }
    if (abs($index - $i) < 5){
        $mse_score = $mse_score + 1;
        #print("MSE +1 val=$value val_index=$i vis=".$visual[$i]." vis_index=$index dist=".abs($index - $i)."\n");
    } elsif (abs($index - $i) > 7){
        $mse_score = $mse_score - 2;
        #print("MSE -2 val=$value val_index=$i vis=".$visual[$i]." vis_index=$index dist=".abs($index - $i)."\n");
    } elsif (abs($index - $i) > 4){
        $mse_score = $mse_score - 1;
    }
    $i++;
}

#Calculate NMSE Ranking's score w.r.t. Visual Ranking
$i = 0;
$index = 0;
my $nmse_score = 0;
foreach my $value (@nmse){
    for (my $j = 0; $j <= $#visual; $j= $j+1){
        if($visual[$j] eq $value){
            $index = $j;
        }
    }
    if (abs($index - $i) < 5){
        $nmse_score = $nmse_score + 1;
    } elsif (abs($index - $i) > 7){
        $nmse_score = $nmse_score - 2;
    } elsif (abs($index - $i) > 4){
        $nmse_score = $nmse_score - 1;
    }
    $i++;
}

print("SSIM vs Visual - Ranking score: ".$ssim_score."\n");
print("PSNR vs Visual - Ranking score: ".$psnr_score."\n");
print("MSE vs Visual - Ranking score: ".$mse_score."\n");
print("NMSE vs Visual - Ranking score: ".$nmse_score."\n");


 