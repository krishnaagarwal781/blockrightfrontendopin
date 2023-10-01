import React, { useContext, useEffect } from "react";
import { BsShareFill } from "react-icons/bs";
import axios from "axios";
import WalletIDMainContext from "../context/walletID/WalletIDMainContext";

const Punk = () => {
  const { fetchedWalletId, fetchRights, setFetchRights } =
    useContext(WalletIDMainContext);

  useEffect(() => {
    const fetchRightsData = async () => {
      try {
        const response = await axios.get(
          "http://127.0.0.1:8000/user/getRights/",
          { params: { walletId: fetchedWalletId.toString() } }
        );
        const rightsData = Object.values(response.data);
        setFetchRights(rightsData);
      } catch (error) {
        console.error(error);
      }
    };

    fetchRightsData();
  }, [fetchedWalletId]);

  const renderRightsCard = (item, index) => {
    const hasCapRights =
      item.capRights &&
      item.capRights.merchantQuantity !== undefined &&
      item.capRights.licenseFees !== undefined;
    const hasTshirtRights =
      item.tshirtRights &&
      item.tshirtRights.merchantQuantity !== undefined &&
      item.tshirtRights.licenseFees !== undefined;
    const hasHoodieRights =
      item.hoodieRights &&
      item.hoodieRights.merchantQuantity !== undefined &&
      item.hoodieRights.licenseFees !== undefined;
    const hasMugRights =
      item.mugRights &&
      item.mugRights.merchantQuantity !== undefined &&
      item.mugRights.licenseFees !== undefined;

    const shouldRenderCard =
      hasCapRights || hasTshirtRights || hasHoodieRights || hasMugRights;

    if (shouldRenderCard) {
      return (
        <div
          key={index}
          className="mt-10 border-2 border-dashed p-3 rounded-lg mb-[3rem] border-cyan-800 hover:bg-slate-600 hover:border-2 hover:border-dashed flex min-h-52"
        >
          <div className="">
            <p className="text-xl font-bold">
              {item.tshirtRights.merchTitle ||
                item.capRights.merchTitle ||
                item.hoodieRights.merchTitle ||
                item.mugRights.merchTitle}
            </p>
            <p className="border-[1.5px] border-b mt-1"></p>
            {/* cap */}
            {item.capRights.merchantQuantity * item.capRights.licenseFees >
              0 && (
              <>
                <div className="flex gap-3 py-2">
                  <div>
                    <p className="text-sm">
                      {item.capRights.merchantQuantity || 0} capRights Minted{" "}
                      {item.capRights.licenseFees || 0} license Fees{" "}
                    </p>
                    <p className="text-sm"> 0 sold, 0 left</p>
                  </div>
                  <div className="leading-0 flex">
                    <div>
                      <p className="text-2xl m-0 p-0 font-semibold">
                        $
                        {item.capRights.merchantQuantity *
                          item.capRights.licenseFees || 0}
                      </p>
                      <p className="text-xs -mt-1 ml-2"> Earned</p>
                    </div>
                    <div className="text-2xl ml-2 mt-3">
                      <BsShareFill />
                    </div>
                  </div>
                </div>
                <p className="border-1 border-b"></p>
              </>
            )}
            {/* Tshirt */}
            {item.tshirtRights.merchantQuantity *
              item.tshirtRights.licenseFees >
              0 && (
              <>
                <div className="flex gap-3 py-2">
                  <div>
                    <p className="text-sm">
                      {item.tshirtRights.merchantQuantity || 0} tshirtRights
                      Minted {item.tshirtRights.licenseFees || 0} license Fees{" "}
                    </p>
                    <p className="text-sm"> 0 sold, 0 left</p>
                  </div>
                  <div className="leading-0 flex">
                    <div>
                      <p className="text-2xl m-0 p-0 font-semibold">
                        $
                        {item.tshirtRights.merchantQuantity *
                          item.tshirtRights.licenseFees || 0}
                      </p>
                      <p className="text-xs -mt-1 ml-2"> Earned</p>
                    </div>
                    <div className="text-2xl ml-2 mt-3">
                      <BsShareFill />
                    </div>
                  </div>
                </div>
                <p className="border-1 border-b"></p>
              </>
            )}
            {/* HoodieRights */}
            {item.hoodieRights.merchantQuantity *
              item.hoodieRights.licenseFees >
              0 && (
              <>
                <div className="flex gap-3 py-2">
                  <div>
                    <p className="text-sm">
                      {item.hoodieRights.merchantQuantity || 0} hoodieRights
                      Minted {item.hoodieRights.licenseFees || 0} license Fees{" "}
                    </p>
                    <p className="text-sm"> 0 sold, 0 left</p>
                  </div>
                  <div className="leading-0 flex">
                    <div>
                      <p className="text-2xl m-0 p-0 font-semibold">
                        $
                        {item.hoodieRights.merchantQuantity *
                          item.hoodieRights.licenseFees || 0}
                      </p>
                      <p className="text-xs -mt-1 ml-2"> Earned</p>
                    </div>
                    <div className="text-2xl ml-2 mt-3">
                      <BsShareFill />
                    </div>
                  </div>
                </div>
                <p className="border-1 border-b"></p>
              </>
            )}
            {/* mugRights */}
            {item.mugRights.merchantQuantity * item.mugRights.licenseFees >
              0 && (
              <>
                <div className="flex gap-3 py-2">
                  <div>
                    <p className="text-sm">
                      {item.mugRights.merchantQuantity || 0} mugRights Minted{" "}
                      {item.mugRights.licenseFees || 0} license Fees{" "}
                    </p>
                    <p className="text-sm"> 0 sold, 0 left</p>
                  </div>
                  <div className="leading-0 flex">
                    <div>
                      <p className="text-2xl m-0 p-0 font-semibold">
                        $
                        {item.mugRights.merchantQuantity *
                          item.mugRights.licenseFees || 0}
                      </p>
                      <p className="text-xs -mt-1 ml-2"> Earned</p>
                    </div>
                    <div className="text-2xl ml-2 mt-3">
                      <BsShareFill />
                    </div>
                  </div>
                </div>
                <p className="border-1 border-b"></p>
              </>
            )}
          </div>
          <div className="h- w-32 ml-5 mt-5">
          <img src={item.imgSrc} alt="" />
        </div>
      </div>
    );
  }
  return null; // Add a semicolon here
};

console.log("Fetch rights here",fetchRights)

if(fetchRights.length == 21 && fetchRights[0]=='U' && fetchRights[1]=='s'){
  return <div className="text-xl font-bold flex items-center justify-center gap-3 w-[32rem]">No rights are approved !!</div>
}
  
return <div>{fetchRights.map(renderRightsCard)}</div>;
};

export default Punk;
